import zipfile
from pathlib import Path
import shutil
import urllib.request as request
from contextlib import closing
import time

import requests
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import tempfile
from tqdm import tqdm
from chromedriver_py import binary_path


def get_content_type(content_type: str):
    return content_type.split(";")[0]


def get_chrome_options(tmp_dir_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.add_experimental_option('prefs', {'download.default_directory': tmp_dir_name})
    return options


def download_easy(url, destination):
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        options = get_chrome_options(tmp_dir_name)
        driver = webdriver.Chrome(executable_path=binary_path, options=options)
        driver.get(url)

        button = driver.find_element_by_xpath("//a[@class='btn btn-default btn-sm']")
        button.click()

        time.sleep(5)

        try:
            accept = driver.find_element_by_xpath('//input[@name="tabs:panel:fe:modalDownload:content:accept"]')
            accept.click()

            time.sleep(3)

            download = driver.find_element_by_xpath('//button[@id="id2d"]')
            download.click()
        except NoSuchElementException:
            pass

        timeout = 0
        while len(list(Path(tmp_dir_name).glob('*.zip'))) == 0:
            time.sleep(5)
            timeout += 5
            if timeout > 600:
                raise ValueError("Download took longer than 10 minutes")

        file_name = list(Path(tmp_dir_name).glob('*.zip'))[0]
        file_name.rename(destination)

        driver.close()


def download_file(url, destination, expected_content_type):
    # Workaround local certificate error for DNB
    verify = '.dnb.nl' not in url
    r = requests.get(url, stream=True, verify=verify)

    content_type = get_content_type(r.headers['content-type'])
    if content_type != expected_content_type:
        raise ValueError(f"Content Type expected '{expected_content_type}' but got '{content_type}' for  {url}")

    total_size = int(r.headers.get('content-length', 0))
    with tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Downloading "{destination}" from {url}') as t:
        with destination.open('wb') as f:
            for data in r.iter_content(chunk_size=1024):
                t.update(len(data))
                f.write(data)

    # Check length if uncompressed
    encoding = r.headers.get('content-encoding', '')
    if total_size != 0 and t.n != total_size and encoding == '':
        destination.unlink()
        raise ValueError("Partial download: file size doesn't match expected size. File removed")


def download_ftp(url, destination):
    with closing(request.urlopen(url)) as r:
        with destination.open('wb') as f:
            shutil.copyfileobj(r, f)


def extract_zip(destination: Path):
    with zipfile.ZipFile(destination) as zip_ref:
        zip_ref.extractall(destination.with_suffix(''))


def download_url(url, destination, content_type):
    if '//easy.dans.knaw.nl/' in url:
        print(f'Downloading "{destination}" from {url}')
        download_easy(url, destination)
    elif url.startswith('ftp://'):
        print(f'Downloading "{destination}" from {url}')
        download_ftp(url, destination)
    else:
        download_file(url, destination, content_type)


def ensure_datasets():
    data_sources = pd.read_csv('datasets.csv')

    data_path = Path('./data')
    data_path.mkdir(exist_ok=True)

    for data_provider, destination_name, url, content_type in data_sources.values.tolist():
        source_path = data_path / data_provider
        source_path.mkdir(exist_ok=True)

        destination = source_path / destination_name
        if not destination.exists():
            try:
                download_url(url, destination, content_type)

                if destination.suffix == ".zip":
                    extract_zip(destination)
            except ValueError as e:
                print(str(e))


ensure_datasets()
