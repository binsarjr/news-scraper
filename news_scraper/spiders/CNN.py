import scrapy, news_scraper.utils as myparser


from bs4 import BeautifulSoup


class CnnSpider(scrapy.Spider):
    name = "CNN"
    allowed_domains = ["cnnindonesia.com"]
    handle_httpstatus_list = [301]
    custom_settings = {
        "ITEM_PIPELINES": {
            "news_scraper.pipelines.DateFilterPipeline": 110,
        },
    }

    def start_requests(self):
        keywords = self.keyword.split(",")
        for keyword in keywords:
            # for cnn
            yield scrapy.Request(
                url=f"https://www.cnnindonesia.com/api/v2/search?query={keyword}&start=0&limit=10",
                headers={"referer": None},
                callback=self.parse_search,
                meta={"keyword": keyword, "source": "cnnindonesia.com"},
            )

    def parse_search(self, response):
        start = int(response.meta.get("start", 0))

        data = response.json()
        if "not found" in data["message"]:
            return

        if len(data["data"]) > 0:
            response.meta["start"] = start + 10
            yield scrapy.Request(
                url=f"https://www.cnnindonesia.com/api/v2/search?query={response.meta['keyword']}&start={response.meta['start']}&limit=10",
                callback=self.parse_search,
                meta=response.meta,
            )

        for article in data["data"]:
            yield scrapy.Request(
                url=article["url"],
                callback=self.parse,
                meta=response.meta,
            )

    def parse(self, response):
        if "location" in response.headers:
            yield scrapy.Request(
                url=response.headers["location"].decode("utf-8"),
                callback=self.parse,
                meta=response.meta,
            )
            return

        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("div", {"class": "detail-text"})

        if article:
            title = soup.find("h1")
            title = title.text if title else ""

            publish_date = soup.select_one("h1+div+div")
            publish_date = publish_date.text if publish_date else ""

            author = soup.find("div", {"class": "author"})
            author = author.text if author else ""

            content = article.text.strip()

            yield {
                "link": response.url,
                "title": title,
                "publish_date": myparser.indo_to_datetime(publish_date),
                "content": f"""
judul: {title}
author: {author}
tanggal: {publish_date}
{content}
""".strip(),
                "source": response.meta["source"],
                "keyword": response.meta["keyword"],
            }
