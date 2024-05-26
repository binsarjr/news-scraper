import scrapy

from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *


class Liputan6Spider(scrapy.Spider):
    name = "Liputan6"
    allowed_domains = ["liputan6.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = f"https://www.liputan6.com/search?order=latest&q={keyword}&type=all"
            if self.since:
                since = string_to_datetime(self.since)
                url += "&from_date=" + since.strftime("%d/%m/%Y")

            if self.until:
                until = string_to_datetime(self.until)
                url += "&to_date=" + until.strftime("%d/%m/%Y")

            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "liputan6.com"},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # for paging in soup.select(".paging > a"):
        #     yield scrapy.Request(
        #         url=paging.get("href"),
        #         callback=self.parse_search,
        #         meta=response.meta,
        #     )

        for article in soup.select(".articles--iridescent-list > article"):
            yield scrapy.Request(
                url=article.select_one("a").get("href"),
                callback=self.parse,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("div", {"class": "article-content-body__item-content"})
        if article:
            title = soup.find("h1")
            title = title.text if title else ""

            publish_date = soup.select_one(
                "time.read-page--header--author__datetime"
            ).attrs["datetime"]

            item = NewsScraperItem()
            item["title"] = title
            item["publish_date"] = indo_to_datetime(publish_date)
            item["content"] = article.text
            item["keyword"] = response.meta["keyword"]
            item["source"] = response.meta["source"]
            item["link"] = response.url

            yield item
