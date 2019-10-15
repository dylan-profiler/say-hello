from pathlib import Path
import shutil
import urllib.request as request
from contextlib import closing

import requests
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm


def download_easy(url, destination):
    # https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.11/
    from selenium import webdriver
    import tempfile
    import time

    print(f'Downloading "{destination}" from {url}')
    with tempfile.TemporaryDirectory() as tmpdirname:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        # options.add_argument("--headless")
        options.add_experimental_option('prefs', {'download.default_directory': tmpdirname})
        driver = webdriver.Chrome(options=options)
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
        while len(list(Path(tmpdirname).glob('*.zip'))) == 0:
            time.sleep(5)
            timeout += 5
            if timeout > 600:
                print("Download took longer than 10 minutes")
                return

        file_name = list(Path(tmpdirname).glob('*.zip'))[0]
        file_name.rename(destination)

        driver.close()


def download_file(url, destination):
    # https://stackoverflow.com/a/37573701/470433
    r = requests.get(url, stream=True)

    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Downloading "{destination}" from {url}')
    with destination.open('wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong")


def download_ftp(url, destination):
    print(f'Downloading "{destination}" from {url}')

    with closing(request.urlopen(url)) as r:
        with destination.open('wb') as f:
            shutil.copyfileobj(r, f)


data_sources = {
    'rdw': {
        'gekentekende_voertuigen.csv': 'https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD',
        'erkende_bedrijven.csv': 'https://opendata.rdw.nl/api/views/5k74-3jha/rows.csv?accessType=DOWNLOAD',
        'carrosserie_uitvoering_klasse.csv': 'https://opendata.rdw.nl/api/views/q7fi-ijjh/rows.csv?accessType=DOWNLOAD',
        'parkeren_parkeergebied.csv': 'https://opendata.rdw.nl/api/views/mz4f-59fw/rows.csv?accessType=DOWNLOAD',
        'parkeren_tijdvak.csv': 'https://opendata.rdw.nl/api/views/ixf8-gtwq/rows.csv?accessType=DOWNLOAD',
        'parkeren_gebied.csv': 'https://opendata.rdw.nl/api/views/adw6-9hsg/rows.csv?accessType=DOWNLOAD'
    },
    'nza': {
        'dbc_zorgproducten.csv': 'https://www.opendisdata.nl/download/csv/01_DBC.csv',
        'zorgactiviteiten.csv': 'https://www.opendisdata.nl/download/csv/02_DBC_PROFIEL.csv',
        'referentietabel_zorgproducten.csv': 'https://www.opendisdata.nl/download/csv/05_REF_ZPD.csv',
        'referentietabel_zorgactiviteiten.csv': 'https://www.opendisdata.nl/download/csv/03_REF_ZAT.csv',
        'referentietabel_specialismen.csv': 'https://www.opendisdata.nl/download/csv/06_REF_SPC.csv',
        'referentietable_diagnoses.csv': 'https://www.opendisdata.nl/download/csv/04_REF_DGN.csv',
        'top100_diagnosegroepen.csv': "https://www.opendisdata.nl/download/diagnose/csv/pat/100/",
        'top100_diagnosegroepen.json': "https://www.opendisdata.nl/download/diagnose/json/pat/100/",
        'top100_zorgproducten.csv': 'https://www.opendisdata.nl/download/zorgproduct/csv/pat/100/',
        'top100_zorgproducten.json': "https://www.opendisdata.nl/download/zorgproduct/json/pat/100/",
    },
    'vektis': {
        'postcodes_2011.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202011%20-%20postcode3.csv',
        'postcodes_2012.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202012%20-%20postcode3.csv',
        'postcodes_2013.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202013%20-%20postcode3.csv',
        'postcodes_2014.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202014%20-%20postcode3.csv',
        'postcodes_2015.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202015%20-%20postcode3.csv',
        'postcodes_2016.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202016%20-%20postcode3.csv',
        'postcodes_2017.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Oud/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202017%20-%20postcode3.csv',
        'gemeentes_2011.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202011%20-%20gemeente.csv',
        'gemeentes_2012.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202012%20-%20gemeente.csv',
        'gemeentes_2013.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202013%20-%20gemeente.csv',
        'gemeentes_2014.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202014%20-%20gemeente.csv',
        'gemeentes_2015.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202015%20-%20gemeente.csv',
        'gemeentes_2016.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202016%20-%20gemeente.csv',
        'gemeentes_2017.csv': 'https://www.vektis.nl/uploads/Docs%20per%20pagina/Open%20Data%20Bestanden/Gemeentebestanden%202011-2016/Vektis%20Open%20Databestand%20Zorgverzekeringswet%202017%20-%20gemeente.csv',
    },
    'duo': {
        'adressen_instellingen_hoger_onderwijs.csv': 'https://onderwijsdata.duo.nl/dataset/f9bee170-0df3-4a9f-b5ee-7b3cd4b36a5f/resource/5f44a1e0-561a-4671-bf96-0bbe78543128/download/instellingenho.csv',
        'prognose_vo_per_instelling.csv': 'https://onderwijsdata.duo.nl/dataset/1dbd001b-92da-4249-833f-6924efd9f684/resource/59622979-241d-4e60-b220-b3ed6ae35a61/download/brin4_prognosesvo.csv',
        'vo_leerlingen.csv': 'https://onderwijsdata.duo.nl/dataset/b7e4a919-a1f7-449e-a98d-707d89ac2a81/resource/e12c0cd1-3637-455d-af2f-718c607fce4a/download/02voins.csv',
        'gediplomeerden_geslaagd_wo.csv': 'https://onderwijsdata.duo.nl/dataset/2a1a78ea-d7fe-4055-8fb5-144144933477/resource/34132d6a-d774-46fb-ac7f-46792a8b778f/download/gediplomeerdengeslwo.csv',
        'personele_bekostiging_bo.csv': 'https://onderwijsdata.duo.nl/dataset/d17b3a97-e107-4068-b242-3b7eacfe3989/resource/777e0694-5a17-4992-8d0a-8240c93ec821/download/persbek_bo_01.csv',
        'referentieniveau.csv': 'https://onderwijsdata.duo.nl/dataset/c9d630ec-5fbd-4a5f-8b10-8f358a91b031/resource/95215baf-0ec4-499b-b0fe-5775d3ae637c/download/brin6_referentieniveau.csv',
        'swv_totaal.csv': 'https://onderwijsdata.duo.nl/dataset/3e719392-b8ca-4b00-bf30-3a7229c435b8/resource/1a65c1a8-fc11-4cf7-aba4-dbd9a2b0473f/download/swv_totaal.csv',
        'swv_geslacht.csv': 'https://onderwijsdata.duo.nl/dataset/3e719392-b8ca-4b00-bf30-3a7229c435b8/resource/a738b63c-606d-4879-b021-2b692263ab21/download/swv_geslacht.csv',
        'swv_leeftijd.csv': 'https://onderwijsdata.duo.nl/dataset/3e719392-b8ca-4b00-bf30-3a7229c435b8/resource/bfb43b91-88e6-4e8f-95a6-c8797e0cde40/download/swv_leeftijd.csv',
        'swv_pc4.csv': 'https://onderwijsdata.duo.nl/dataset/3e719392-b8ca-4b00-bf30-3a7229c435b8/resource/08cbcbe3-9a7f-4492-a015-b60b2a81c10c/download/swv_pc4.csv',
    },
    'cbr': {
        'opleidingsdata_jul2018_jun2019.csv': 'https://www.cbr.nl/web/file?uuid=30efae66-39d6-425a-a8db-6bbe026f044a&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=11696',
        'examens_jul2018_jun2019.csv': 'https://www.cbr.nl/web/file?uuid=22431038-3c85-4f23-8203-ce90afbecc94&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=11702',
        'diplomas_jul2018_jun2019.csv': 'https://www.cbr.nl/web/file?uuid=3c7989d4-cd87-43cd-9ea7-fbaffe93440f&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=11875',
        'opleidingsdata_jul2017_jun2018.csv': 'https://www.cbr.nl/web/file?uuid=191d04ef-02d9-4948-b691-4e3766dfa844&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=8120',
        'examens_jul2017_jun2018.csv': 'https://www.cbr.nl/web/file?uuid=68b3852b-22e6-430b-a7c3-06b129a61efb&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=8119',
        'diplomas_jul2017_jun2018.csv': 'https://www.cbr.nl/web/file?uuid=2cf4a8fe-e4d7-4711-959e-e13bba0b417d&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=8118',
    },
    'cbs': {
        'kerncijfers_bevolking_data.json': 'https://opendata.cbs.nl/ODataApi/odata/37296ned/TypedDataSet',
        'kerncijfers_bevolking_table_info.json': 'https://opendata.cbs.nl/ODataApi/odata/37296ned/TableInfos',
        'agrarische_bedrijven_table_info.json': 'https://opendata.cbs.nl/ODataFeed/odata/71904ned/TableInfos',
        'agrarische_bedrijven_data.json': 'https://opendata.cbs.nl/ODataFeed/odata/71904ned/TypedDataSet',
        'kerncijfers_recht_table_info.json': 'https://opendata.cbs.nl/ODataFeed/odata/70229ned/TableInfos',
        'kerncijfers_recht_data.json': 'https://opendata.cbs.nl/ODataFeed/odata/70229ned/TypedDataSet',
        'verdachten_table_info.json': 'https://opendata.cbs.nl/ODataFeed/odata/81960NED/TableInfos',
        'verdachten_data.json': 'https://opendata.cbs.nl/ODataFeed/odata/81960NED/TypedDataSet',
        'hypotheken_table_info.json': 'https://opendata.cbs.nl/ODataApi/OData/70231ned/TableInfos',
        'hypotheken_data.json': 'https://opendata.cbs.nl/ODataApi/OData/70231ned/TypedDataSet',
    },
    'georegister': {
        'rijkswaterstaat_districten.json': 'https://geoservices.rijkswaterstaat.nl/apps/geoserver/regiogebieden_rijkswaterstaat/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=rijkswaterstaat_districten_nat&outputFormat=json',
        'rijkswaterstaat_districten.csv': 'https://geoservices.rijkswaterstaat.nl/apps/geoserver/regiogebieden_rijkswaterstaat/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=rijkswaterstaat_districten_nat&outputFormat=csv',
        'rijkswaterstaat_districten.gml': 'https://geoservices.rijkswaterstaat.nl/apps/geoserver/regiogebieden_rijkswaterstaat/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=rijkswaterstaat_districten_nat&outputFormat=text/xml;+subtype=gml/2.1.2',
    },
    'radboud': {
        'meta_analysis_spoken_input.zip': 'https://files.osf.io/v1/resources/92vfw/providers/osfstorage/?zip=',
        'faces_traits.zip': 'https://files.osf.io/v1/resources/z56th/providers/osfstorage/?zip=',
        'eye_tracking_trustworthiness.zip': 'https://files.osf.io/v1/resources/3wabp/providers/osfstorage/?zip=',
        'classifying_acoustic_signals.xls': 'https://osf.io/em6h5/download',
        'nells.zip': 'https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:59831/tab/2',
        'sarcasm.zip': 'https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:65746/tab/2',
        'emotion.zip': 'https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:73774/tab/2',
        'eindhoven_population.zip': 'https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:1341/tab/2',
        'camelyon_stage_labels.csv': 'ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100439/CAMELYON17/training/stage_labels.csv',
        'camelyon_lesion_annotations.zip': 'ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100439/CAMELYON17/training/lesion_annotations.zip',
        'camelyon_center_0_patient_000.zip': 'ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100439/CAMELYON17/training/center_0/patient_000.zip',
        'camelyon_submission_example.csv': 'ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100439/CAMELYON17/testing/evaluation/submission_example.csv',
    },
    'cjib': {
        'snelheidsovertredingen_2018.csv': 'https://data.overheid.nl/OpenDataSets/CJIB/SnelheidsovertredingenWahv2018.csv',
        'snelheidsovertredingen_2019t1.csv': 'https://data.overheid.nl/sites/default/files/dataset/6741aa95-aab4-4e68-95d0-c50ec4fa95eb/resources/Snelheidsovertredingen%202019%201e%20tertiaal.csv',
        'instroom_zaken_2018.csv': 'https://data.overheid.nl/OpenDataSets/CJIB/Instroomfeitgecodeerdezaken2018.csv',
        'trajectcontrole_2018.csv': 'https://data.overheid.nl/OpenDataSets/CJIB/Trajectcontrolesystemen2018.csv',
        'trajectcontrole_2019t1.csv': 'https://data.overheid.nl/sites/default/files/dataset/e8da471f-38cf-45f9-95c0-002735dfbd91/resources/Traject%20controle%20systemen%202019%201e%20tertiaal.csv',
    },
    'dnb': {
        'rentetarieven_ecb.json': 'https://statistiek.dnb.nl/downloads/index.aspx#/details/statistiek/dataset/375ba6dd-3665-40ea-83eb-e5b190b7615b/resource/6e8be666-3a26-43e0-8396-3868b83b934d',
        'ondernemingspensioenfondsen.json': 'https://statistiek.dnb.nl/downloads/index.aspx#/details/statistiek/dataset/6449fcee-2105-417f-865c-7810aadd81c1/resource/570798eb-70cc-48a8-8005-146c91fc45ab',
        'bedrijfstakpensioenfondsen.json': 'https://statistiek.dnb.nl/downloads/index.aspx#/details/statistiek/dataset/6449fcee-2105-417f-865c-7810aadd81c1/resource/38f2013f-64a1-414f-a13b-926a76133690',
    }
}

data_path = Path('./data')
data_path.mkdir(exist_ok=True)

for source_name, data in data_sources.items():
    source_path = data_path / source_name
    source_path.mkdir(exist_ok=True)
    for dataset_name, url in data.items():
        if not (source_path / dataset_name).exists():
            if '//easy.dans.knaw.nl/' in url:
                download_easy(url, source_path / dataset_name)
            elif url.startswith('ftp://'):
                download_ftp(url, source_path / dataset_name)
            else:
                download_file(url, source_path / dataset_name)
