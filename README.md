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


# Research
## Background

In today's digital era, news information has become one of the main sources for society to obtain the latest updates on various events and developments worldwide. The vast volume of information published daily by various online media presents its own challenges in managing and accessing data efficiently. A scraper tool designed to automate news data collection can be an effective solution to address these challenges.

Fragmentation of news sources is a specific issue arising from the multitude of websites presenting information in different formats and structures. This fragmentation complicates the data collection and analysis process, requiring additional effort to standardize information from various sources. With a scraper tool, data can be collected in a consistent format, facilitating the analysis and integration of data from diverse sources.

Another emerging issue is data accessibility, especially from sites that do not provide APIs or easily accessible data retrieval services. This limitation forces researchers and analysts to seek alternative methods for systematic data collection. Scraping becomes a solution to overcome these limitations, allowing data extraction directly from web pages.

Additionally, data consistency and standardization pose challenges in collecting news information. Variations in information presentation, such as date formats and author name writing, require data normalization for accurate analysis. An effective scraper tool can automatically normalize data, maintaining the consistency and accuracy of the collected data.

Access restrictions imposed by some news sites, such as limits on the number of data requests per day or per IP, are also common issues in large-scale data collection. An advanced scraper tool can overcome these limitations through techniques like using proxies or IP rotation, ensuring data can be collected without violating set restrictions.

Privacy policies and copyrights are crucial aspects to consider in the scraping process. The use of scraper tools must comply with the privacy policies and copyrights of the source sites, ensuring that data collection is conducted legally and ethically. This research will consider the legality and ethics of the scraping process to ensure compliance with existing regulations.

Error handling and network failures are technical challenges that need to be addressed in developing a scraper tool. Scraping is prone to network errors and changes in site structure, necessitating effective error management mechanisms. A well-designed scraper tool should handle network failures and automatically adapt to changes in website structure.

To ensure that the collected data is always up-to-date, the scraper tool must be capable of collecting news information in real-time or near real-time. Continuous updates of information require a tool that can operate continuously and efficiently. This is essential to ensure that the data collected remains relevant and useful for further analysis.

The proposed solution in this research is the development of a scraper tool that can automate the collection of news data from various websites while addressing the identified challenges. Reviewing existing scraping solutions will aid in designing a more efficient and effective tool. Implementing this tool is expected to have a long-term impact on news data collection and analysis, facilitating researchers and analysts in obtaining the necessary information more quickly and accurately.

In the long run, an effective scraper tool can enhance efficiency and accuracy in news data collection, adding value to various fields of research and analysis. The use of this tool can save time and resources and enable large-scale data analysis that was previously challenging to perform manually. Thus, this research is expected to make a significant contribution to the field of news data collection and analysis.