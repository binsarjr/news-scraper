# News Scraper
News Scraper is a powerful and flexible tool designed to scrape news articles from multiple prominent sources in Indonesia. This project is perfect for those who need to gather and analyze news data from various outlets.

## Supported Sources
The scraper can collect news from the following sources:
- [Kompas](https://kompas.com/)
- [Tribun](https://www.tribunnews.com/)
- [Detik](https://www.detik.com/)
- [Cnnindonesia](https://www.cnnindonesia.com/)
- [Viva](https://www.viva.co.id/)
- [Okezone](https://okezone.com/)
- [Idntimes](https://www.idntimes.com/)
- [Mongabay](https://www.mongabay.co.id/)
- [Kontan](https://www.kontan.co.id/)
- [Liputan6](https://www.liputan6.com/)


## Requirements
To get started with this project, you'll need to have [Poetry](https://python-poetry.org/)  Installed on your system.

## Installation
Clone the repository and install the required dependencies using Poetry:

```bash
poetry install
```

## Usage

You can run the scraper using Scrapy via Poetry or the main Python script. Here are a few usage examples:

### Using Scrapy
To scrape news articles from CNN Indonesia with a specific keyword and save the results to a CSV file:

```bash
poetry run scrapy crawl CNN -a keyword=indonesia -o data.csv
```

To include a date range in your search:

```bash
poetry run scrapy crawl CNN -a keyword=indonesia -a since=2023-01-01 -a until=2023-01-31 -o data.csv
```


### Using the Main Script

Alternatively, you can run the main Python script directly. This script provides a more interactive way to set your search parameters:

```bash
poetry run python main.py -q indonesia --since 2023-01-01 --until 2023-01-31 --output data.csv
```
The main script supports the following arguments:
- `-q`, `--query`: The search query (required, multiple values allowed).
- `--since`, : The start date for the search (optional).
- `--until`, : The end date for the search (optional).
- `--output`: The output file (optional, supports .json, .csv, and .xml formats).

### Example

To search for news articles about "indonesia" from January 1, 2023, to January 31, 2023, and save the results to a CSV file, you can use:

```bash
poetry run python main.py -q indonesia --since 2023-01-01 --until 2023-01-31 --output data.csv
```

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements.
