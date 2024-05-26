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