# Say hello

This repository allows to download data for demonstration of DYLANs capabilities in practice.

The sample tries to be representative by sourcing data from Dutch data providers in various sectors Healthcare, Finance, Science, Education, Traffic, Legislative and Infrastructure.

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


## Usage

You can download the datasets by running:

```bash
python data_sources.py
```

## Installation

Installation for Python 3 requires two steps:

1. Install the required Python packages.
    - Option 1: create a conda environment `conda env create -f env.yml`
    - Option 2: install via pip `pip install -U tqdm selenium` 

2. Install Chrome/Chromium and [ChromeDriver](https://chromedriver.chromium.org/downloads) 
