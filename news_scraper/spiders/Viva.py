import scrapy, re, json

from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *
from urllib.parse import urlsplit


class VivaSpider(scrapy.Spider):
    name = "Viva"
    allowed_domains = ["viva.co.id"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.NewsPipeline": 100,
            "news_scraper.pipelines.DateFilterPipeline": 110,
            "news_scraper.pipelines.SentimentPipeline": 200,
            "news_scraper.pipelines.PostgresPipeline": 300,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = f"https://www.viva.co.id/search?q={keyword}"

            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "viva.co.id", "page": 1},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select(".article-list-row"):
            a = article.select_one("a")

            yield scrapy.Request(
                url=a.get("href"),
                callback=self.parse,
                meta=response.meta,
            )

        if len(soup.select(".article-list-row")) > 0:
            if "token" in response.meta:
                token = response.meta["token"]
            else:
                token = re.search(
                    r'token\s{0,}:\s{0,}"([^"]+)"', response.text, re.DOTALL
                ).group(1)
            response.meta["page"] += 1
            response.meta["token"] = token
            yield scrapy.Request(
                url="https://www.viva.co.id/request/load-more-search",
                method="POST",
                headers={
                    "content-type": "application/json",
                },
                body=json.dumps(
                    {
                        "keyword": response.meta["keyword"],
                        "ctype": "art",
                        "page": response.meta["page"],
                        "record_count": 12,
                        "_token": token,
                    }
                ),
                callback=self.parse_search,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", {"class": "main-content-title"}).text.strip()
        publish_date = soup.find("div", {"class": "main-content-date"}).text.strip()
        author = soup.find("div", {"class": "main-content-author"}).text.strip()

        content = soup.find("div", {"class": "main-content-detail"}).text.strip()

        item = NewsScraperItem()
        item["title"] = title
        item["publish_date"] = indo_to_datetime(publish_date)
        item["author"] = author
        item["content"] = content
        item["keyword"] = response.meta["keyword"]
        item["source"] = response.meta["source"]
        item["link"] = response.url

        yield item
