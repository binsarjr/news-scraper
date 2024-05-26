import scrapy
import news_scraper.utils as myparser
import logging, re, dateparser
from urllib.parse import *
from modules import google_cse
from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem


class KompasSpider(scrapy.Spider):
    name = "Kompas"
    allowed_domains = ["kompas.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS": 20,
        "DOWNLOAD_DELAY": 2,
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    cx_token = "partner-pub-9012468469771973:uc7pie-r3ad"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.__params = google_cse.get_params(self.cx_token)

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            # search mode by google search
            try:
                yield scrapy.Request(
                    callback=self.request_google_search,
                    method="GET",
                    meta={"keyword": keyword, "source": "kompas.com"},
                    **google_cse.make_request_args(
                        keyword,
                        params=self.__params,
                    ),
                )
            except Exception as e:
                logging.error(str(e))
                logging.error("Error when requesting google search")
                logging.error("Keyword: " + keyword)

    def request_google_search(self, response):
        # Find the match using regex
        data = google_cse.extract_google_search_cse(response.text)

        if len(data["cursor"]["pages"]) > 0:
            for page in data["cursor"]["pages"]:
                response.meta["page"] = page
                yield scrapy.Request(
                    callback=self.request_google_search,
                    method="GET",
                    meta=response.meta,
                    **google_cse.make_request_args(
                        keyword=response.meta["keyword"],
                        page=int(page["label"]),
                        params=self.__params,
                    ),
                )

        for result in data["results"]:
            url = urlparse(result["unescapedUrl"])
            if url.query == "":
                url = url._replace(query="page=all")
            else:
                url = url._replace(query=f"{url.query}&page=all")
            url = urlunparse(url)

            yield scrapy.Request(
                callback=self.parse,
                method="GET",
                meta=response.meta,
                url=url,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("div", {"class": "read__content"})

        if article:
            title = soup.find("h1", {"class": "read__title"})
            title = title.text if title else ""

            publish_date = soup.find("div", {"class": "read__time"})
            for child in publish_date.find_all():
                child.decompose()
            publish_date = publish_date.text if publish_date else ""
            publish_date = publish_date.strip()
            publish_date = re.sub(r"^\s*-\s*", "", publish_date)

            author = soup.find("div", {"class": "read__author"})
            author = author.text if author else ""

            content = article.text.strip()

            item = NewsScraperItem()
            item["title"] = title
            item["publish_date"] = myparser.indo_to_datetime(publish_date)
            item["author"] = author
            item["content"] = (
                f"""
judul: {title}
author: {author}
tanggal: {publish_date}
{content}
""".strip()
            )
            item["keyword"] = response.meta["keyword"]
            item["source"] = response.meta["source"]
            item["link"] = response.url

            yield item
