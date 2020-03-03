import _csv
from pathlib import Path
import json

import pandas as pd

from pandas_profiling import ProfileReport


def generate_report(report_file, df, title):
    report = ProfileReport(df, title=title)
    report.to_file(report_file)


def profile_datasets():
    data_sources = pd.read_csv('datasets.csv')
    data_path = Path('./data')
    report_path = Path('./reports')

    for data_provider, destination_name, url, content_type in data_sources.values.tolist():
        source_path = data_path / data_provider
        destination = source_path / destination_name

        report_file = (report_path / data_provider / destination_name).with_suffix('.html')
        if not report_file.exists():
            report_file.parent.mkdir(exist_ok=True)
            title = f"{data_provider} / {destination_name}"

            if destination.suffix == ".csv":
                try:
                    df = pd.read_csv(destination, sep=None, engine='python', nrows=1000)
                    generate_report(report_file, df, title)
                except (pd.errors.ParserError, _csv.Error):
                    print(f"Could not read csv '{destination}'")
                except FileNotFoundError:
                    print(f"File '{destination}' does not exist")
            elif destination.suffix == ".xls":
                df = pd.read_excel(destination)
                generate_report(report_file, df, title)
            elif destination.suffix == ".json":
                if data_provider == "cbs":
                    with destination.open(encoding='utf-8-sig') as f:
                        data = json.load(f)

                    df = pd.DataFrame(data['value'])
                    generate_report(report_file, df, title)
                else:
                    print(f"Data provider '{data_provider}' not supported")
            else:
                print(f"Suffix {destination.suffix} not yet supported")


profile_datasets()
