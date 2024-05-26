import scrapy

from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *
from urllib.parse import urlsplit


class OkezoneSpider(scrapy.Spider):
    name = "Okezone"
    allowed_domains = ["okezone.com"]

    custom_settings = {
        "ITEM_PIPELINES": {"news_scraper.pipelines.DateFilterPipeline": 110},
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = (
                "https://search.okezone.com/searchsphinx/loaddata/article/{}/0".format(
                    keyword
                )
            )
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "okezone.com"},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select(".listnews"):
            a = article.select_one("a")
            href = a.get("href")

            yield scrapy.Request(
                url=href,
                callback=self.parse,
                meta=response.meta,
            )
        for li in soup.select("#article-pagination li"):
            a = li.select_one("a")
            href = a.get("href")
            if "javascript:void" in href:
                continue

            start = href.split("/")[-1]
            url = f"https://search.okezone.com/searchsphinx/loaddata/article/{response.meta['keyword']}/{start}"

            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one(".title h1").text.strip()
        publish_date = soup.select_one(".reporter b").text.strip()
        author = soup.select_one(".reporter a").text.strip()
        content = soup.select_one("#contentx").text.strip()

        publish_date = publish_date.replace("'", "")

        item = NewsScraperItem()
        item["title"] = title
        item["publish_date"] = indo_to_datetime(publish_date)
        item["author"] = author
        item["content"] = content
        item["keyword"] = response.meta["keyword"]
        item["source"] = response.meta["source"]
        item["link"] = response.url

        yield item
