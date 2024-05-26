import scrapy

from bs4 import BeautifulSoup
from news_scraper.items import NewsScraperItem
from news_scraper.utils import *
from urllib.parse import urlsplit


class KontanSpider(scrapy.Spider):
    name = "Kontan"
    allowed_domains = ["kontan.co.id"]
    # handle_httpstatus_list = [403]

    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            url = f"https://www.kontan.co.id/search?search={keyword}"

            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "kontan.co.id"},
            )

    def parse_search(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select(".list-berita ul > li"):
            a = article.select_one("a")

            href = a.get("href")
            if href.startswith("//"):
                href = "https:" + href
            yield scrapy.Request(
                url=href,
                callback=self.parse,
                meta=response.meta,
            )

        for paging in soup.select("ul.cd-pagination > li:not(.button)"):
            if paging.find("a") is None:
                continue

            href = paging.find("a").get("href")
            url_components = urlsplit(response.url)
            href = url_components.scheme + "://" + url_components.netloc + href
            yield scrapy.Request(
                url=href,
                callback=self.parse_search,
                meta=response.meta,
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", {"class": "jdl_dtl"})
        title = title.text if title else ""

        content = soup.select_one('div[itemprop="articleBody"]')
        content = content.text.strip()

        author = soup.select_one("#penulis")
        if author is not None:
            author = author.text.strip()

        publish_date = soup.select_one("h1+div")

        for child in publish_date.find_all():
            child.decompose()

        publish_date = publish_date.text if publish_date else ""

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
