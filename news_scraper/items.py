# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    title = scrapy.Field()
    publish_date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    keyword = scrapy.Field()
    source = scrapy.Field()
    link = scrapy.Field()
