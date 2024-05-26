# News Scraper

## Source
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
- [Poetry](https://python-poetry.org/)

## Installation
```bash
poetry install
```

## Usage
```bash
poetry run scrapy crawl CNN -a keyword=indonesia -o data.csv
```

with date

```bash
poetry run scrapy crawl CNN -a keyword=indonesia -a since=2023-01-01 -a until=2023-01-31 -o data.csv
```



or 

```bash
poetry run python main.py
```