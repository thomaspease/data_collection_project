# Data collection project

A web scraper that uses Selenium to scrape data from websites, particularly configured to scrape data on commercial property from Rightmove.

## How to set up

Ensure that you have Miniconda installed on your device (https://docs.conda.io/en/latest/miniconda.html). Create a project environment from the config file, and make sure that it is activated.

```C
conda env create -f environment.yml -n new-conda-environment

conda activate new-conda-environment
```

To run the scraper, simply run the file `rightmove.py`

## Features

- The parent class `Scraper` is website agnostic
- The child class `RightmoveScraper` contains methods specifically for scraping data from commercial property adverts on Rightmove.co.uk.
- The data is exported to a .json file

## Configuration

There are two important configuration settings, found within the `if __name__ == "__main__":` block:

- `start_url` is the page that the scraper will begin on. By going on Rightmove and searching for properties with particular characteristics (e.g. in London, under £1 million), you can then replace the URL.
- `pages_to_scrape` how many pages the scraper will grab links from

## TODOs

[ ] Finish unit tests
[ ] Push data to an RDS database SQLAlchemy and PostgreSQL
[ ] Containerise using Docker and push to EC2 instance
