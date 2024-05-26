# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
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

    def process_item(self, item, spider):
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
        if item["created_at"] is None:
            raise DropItem("Item has no created_at")

        if not is_valid_datetime(item["created_at"]):
            spider.crawler.engine.close_spider(
                self, "Item created_at has invalid format datetime"
            )

        item["created_at"] = dateparser.parse(
            item["created_at"],
            languages=["en"],
            settings={"TIMEZONE": "Asia/Jakarta"},
        )

        if item["created_at"] is None:
            spider.crawler.engine.close_spider(
                self,
                "Item created_at failed to parse datetime with dateparser, check again",
            )

        if since is not None:
            if item["created_at"] < since:
                raise DropItem("Item created before since")

        if until is not None:
            if item["created_at"] > until:
                raise DropItem("Item created after until")

        if since is not None and until is not None:
            if item["created_at"] < since or item["created_at"] > until:
                raise DropItem("Item created not in range")

        return item
