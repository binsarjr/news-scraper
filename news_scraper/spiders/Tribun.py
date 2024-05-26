import scrapy
import logging, re, dateparser

from news_scraper.utils import *

from urllib.parse import *

from modules import google_cse
from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem


class TribunSpider(scrapy.Spider):
    name = "Tribun"

    allowed_domains = ["tribunnews.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS": 20,
        "DOWNLOAD_DELAY": 2,
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    cx_token = "4593c3f3750fa44b5"

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
                    meta={"keyword": keyword, "source": "tribunnews.com"},
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
        article = soup.find("div", {"id": "article"})

        if article:
            title = soup.find("h1", {"id": "arttitle"})
            title = title.text if title else ""

            publish_date = soup.find("time")
            publish_date = publish_date.text if publish_date else ""

            author = article.find("h5", {"id": "penulis"})
            if author:
                author = author.text.strip()
                author = re.sub(r"\s{2,}", " ", author)
                author = re.sub(r"\n", " ", author)
                author = author.strip()
            else:
                author = ""

            content = article.find("div", {"class": "txt-article"}).text.strip()

            item = NewsScraperItem()
            item["title"] = title
            item["publish_date"] = indo_to_datetime(publish_date)
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
        # mungkin tag atau yang lain
        else:
            if "/tag" in response.url:
                # spider for another tag
                for a in soup.select("#paginga a[href]"):
                    url = a["href"]
                    yield scrapy.Request(
                        url=url, callback=self.parse, meta=response.meta
                    )

                for li in soup.select("div.content ul.lsi > li"):
                    url = li.select_one("a")["href"]
                    yield scrapy.Request(
                        url=url, callback=self.parse, meta=response.meta
                    )
