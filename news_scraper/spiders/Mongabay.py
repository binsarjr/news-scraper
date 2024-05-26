import scrapy
import re
from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *
from urllib.parse import urlsplit


class MongabaySpider(scrapy.Spider):
    name = "Mongabay"
    allowed_domains = ["mongabay.co.id"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = "https://www.mongabay.co.id/page/1?s=" + keyword
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "mongabay.co.id"},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.select("article.post-news"):
            a = article.select_one(".post-title-news a")
            href = a.get("href")

            yield scrapy.Request(url=href, callback=self.parse, meta=response.meta)

        for paging in soup.select("a.page-numbers"):
            href = paging.get("href")

            if href is None:
                continue

            yield scrapy.Request(
                url=href,
                callback=self.parse_search,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("#headline .article-headline h1").text.strip()
        content = soup.select_one("#main").text.strip()

        author = soup.select_one(".single-article-meta a").text.strip()

        el = soup.select_one(".single-article-meta")
        for i in el.find_all():
            i.decompose()

        publish_date = el.text.strip()
        splitted = publish_date.split(" ")
        publish_date = f"{splitted[-3]} {splitted[-2]} {splitted[-1]}"

        publish_date = indo_to_datetime(publish_date, format="%d %B %Y")

        item = NewsScraperItem()
        item["title"] = title
        item["link"] = response.url
        item["content"] = content
        item["author"] = author
        item["publish_date"] = publish_date
        item["keyword"] = response.meta["keyword"]
        item["source"] = response.meta["source"]

        yield item
