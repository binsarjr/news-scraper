import scrapy


from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *
from urllib.parse import urlsplit


class IdntimesSpider(scrapy.Spider):
    name = "Idntimes"
    allowed_domains = ["idntimes.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = f"https://www.idntimes.com/search-ajax?keyword={keyword}&type=article&page=1"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "idntimes.com", "page": 1},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select(".box-list"):
            a = article.select_one("a")
            href = a.get("href")

            if "?" in href:
                href += "&page=all"
            else:
                href += "?page=all"

            yield scrapy.Request(
                url=href,
                callback=self.parse,
                meta=response.meta,
            )

        response.meta["page"] += 1
        url = f"https://www.idntimes.com/search-ajax?keyword={response.meta['keyword']}&type=article&page={response.meta['page']}"
        yield scrapy.Request(
            url=url,
            callback=self.parse_search,
            meta=response.meta,
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("h1.title-text").text.strip()
        publish_date = soup.select_one("time.date").text.strip()
        content = soup.select_one("#article-content").text.strip()

        author = soup.select_one(".author-name").text.strip()

        item = NewsScraperItem()
        item["title"] = title
        item["publish_date"] = indo_to_datetime(publish_date, format="%d %b %Y")
        item["content"] = content
        item["author"] = author
        item["keyword"] = response.meta["keyword"]
        item["source"] = response.meta["source"]
        item["link"] = response.url

        yield item
