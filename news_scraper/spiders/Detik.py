import scrapy
from news_scraper.items import NewsScraperItem
from bs4 import BeautifulSoup
from news_scraper.utils import *


class DetikSpider(scrapy.Spider):
    name = "Detik"
    allowed_domains = ["detik.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware": 500,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = f"https://www.detik.com/search/searchall?query={keyword}&siteid=2&sortby=time&page=1"
            if getattr(self, "since", None):
                since = string_to_datetime(self.since)
                url += "&fromdatex=" + since.strftime("%d/%m/%Y")

            if getattr(self, "until", None):
                until = string_to_datetime(self.until)
                url += "&todatex=" + until.strftime("%d/%m/%Y")

            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "detik.com"},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        for paging in soup.select(".paging > a"):
            yield scrapy.Request(
                url=paging.get("href"),
                callback=self.parse_search,
                meta=response.meta,
            )

        for article in soup.select(".list-berita > article"):
            yield scrapy.Request(
                url=article.select_one("a").get("href"),
                callback=self.parse,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("div", {"class": "detail__body-text"})
        if article:
            title = soup.find("h1")
            title = title.text if title else ""

            publish_date = soup.select_one("h1+div+div")
            publish_date = publish_date.text if publish_date else ""

            author = soup.select_one("div.detail__author")
            author = author.text if author else ""

            content = soup.select_one("div.detail__body-text")
            content = content.text if content else ""

            item = NewsScraperItem()
            item["title"] = title
            item["publish_date"] = indo_to_datetime(publish_date)
            item["author"] = author
            item["content"] = content
            item["keyword"] = response.meta["keyword"]
            item["source"] = response.meta["source"]
            item["link"] = response.url

            yield item
