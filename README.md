# Say hello

This repository allows to download data for demonstration of DYLANs capabilities in practice.

The sample tries to be representative by sourcing data from (primarily) Dutch data providers in various sectors Healthcare, Finance, Science, Education, Traffic, Legislative and Infrastructure.

Providers:

- [CBR](https://www.cbr.nl/)
- [CBS](https://www.cbs.nl)
- [DUO](https://duo.nl/)
- [Nationaal Georegister](https://www.nationaalgeoregister.nl/)
- [NZa](https://www.nza.nl/)
- [CJIB](https://www.cjib.nl/)
- [DNB](https://www.dnb.nl/)
- [RDW](https://www.rdw.nl/)
- [Vektis](https://www.vektis.nl/)
- [Radboud University](https://www.ru.nl/)
- [Simula](https://datasets.simula.no/)

## Usage

You can download the datasets by running:

```bash
python data_sources.py
```

## Installation

Installation for Python 3 requires two steps:

1. Install the required Python packages.
    - Option 1: create a conda environment `conda env create -f env.yml`
    - Option 2: install the requirements as listen in `env.yml` via pip `pip install -U [requirement]` 

2. Install Chrome/Chromium and [ChromeDriver](https://chromedriver.chromium.org/downloads) 

## Example usage

The [`type_analysis`](/type_analysis) directory contains jupyter notebooks with analyses of the data types of each dataset. These are also an excellent reference implementation for loading the sets.

The [`profile.py`](/profile.py) script generates exploratory data analysis reports for the datasets.