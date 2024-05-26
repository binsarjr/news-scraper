# Define your item pipelines here

#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news_scraper.items import NewsScraperItem
import dateparser

from news_scraper.utils import is_valid_datetime

from scrapy.exceptions import DropItem


class TwitterScraperPipeline:
    def process_item(self, item, spider):
        return item


class DateFilterPipeline:
    """
    Filter item based on date (column: created_at)
    """

    def process_item(self, item: NewsScraperItem, spider):
        since = (
            dateparser.parse(
                spider.since,
                languages=["en"],
                settings={"TIMEZONE": "Asia/Jakarta"},
            )
            if getattr(spider, "since", None) is not None
            else None
        )
        until = (
            dateparser.parse(
                spider.until,
                languages=["en"],
                settings={"TIMEZONE": "Asia/Jakarta"},
            )
            if getattr(spider, "until", None) is not None
            else None
        )

        # verify date with since and until but two of this can be None
        if item["publish_date"] is None:
            raise DropItem("Item has no created_at")

        if not is_valid_datetime(item["publish_date"]):
            spider.crawler.engine.close_spider(
                self, "Item created_at has invalid format datetime"
            )

        item["publish_date"] = dateparser.parse(
            item["publish_date"],
            languages=["en"],
            settings={"TIMEZONE": "Asia/Jakarta"},
        )

        if item["publish_date"] is None:
            spider.crawler.engine.close_spider(
                self,
                "Item created_at failed to parse datetime with dateparser, check again",
            )

        if since is not None:
            if item["publish_date"] < since:
                raise DropItem("Item created before since")

        if until is not None:
            if item["publish_date"] > until:
                raise DropItem("Item created after until")

        if since is not None and until is not None:
            if item["publish_date"] < since or item["publish_date"] > until:
                raise DropItem("Item created not in range")

        return item
