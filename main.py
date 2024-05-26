import argparse
from news_scraper.utils import *

parser = argparse.ArgumentParser(description="News Crwaler")

parser.add_argument(
    "-q", "--query", type=str, nargs="+", required=True, help="Search query"
)

parser.add_argument("--since", type=str, help="Date from")
parser.add_argument("--until", type=str, help="Date until")

parser.add_argument("--output", type=str, help="Output file")


args = parser.parse_args()
clear_console()

print("News Crawler")
print("Search query:")
print("\n")
for i, query in enumerate(args.query):
    print(f"{i+1}. {query}")
print("\n")


if args.since:
    print(f"Data processed from : {args.since}")

if args.until:
    print(f"Data processed until : {args.until}")


print("\n")

if query_yes_no("Are you sure?") is False:
    exit()


from scrapy.crawler import CrawlerProcess
from news_scraper.spiders.CNN import CnnSpider
from news_scraper.spiders.Kompas import KompasSpider
from news_scraper.spiders.Tribun import TribunSpider
from news_scraper.spiders.Detik import DetikSpider
from news_scraper.spiders.Liputan6 import Liputan6Spider
from news_scraper.spiders.Kontan import KontanSpider

# from news_scraper.spiders.Viva import VivaSpider
from news_scraper.spiders.Okezone import OkezoneSpider
from news_scraper.spiders.Idntimes import IdntimesSpider
from news_scraper.spiders.Mongabay import MongabaySpider


spider_args = {
    "keyword": ",".join(args.query),
    "since": args.since,
    "until": args.until,
}


spider_settings = {
    "DUPEFILTER_DEBUG": True,
    # "LOG_LEVEL": "ERROR",
    # "CONCURRENT_REQUESTS": 1,
    # "DOWNLOAD_DELAY": 5,
}

if args.output:
    spider_settings["FEED_URI"] = args.output
    if args.output.endswith(".json"):
        spider_settings["FEED_FORMAT"] = "json"
    elif args.output.endswith(".csv"):
        spider_settings["FEED_FORMAT"] = "csv"
    elif args.output.endswith(".xml"):
        spider_settings["FEED_FORMAT"] = "xml"
    else:
        print("Unsupported file format. Supported formats are: .json, .csv, .xml")
        exit()

process = CrawlerProcess(spider_settings)

# process.crawl(VivaSpider, **spider_args)
process.crawl(KontanSpider, **spider_args)
process.crawl(Liputan6Spider, **spider_args)
process.crawl(DetikSpider, **spider_args)
process.crawl(CnnSpider, **spider_args)
process.crawl(KompasSpider, **spider_args)
process.crawl(TribunSpider, **spider_args)
process.crawl(OkezoneSpider, **spider_args)
process.crawl(IdntimesSpider, **spider_args)
process.crawl(MongabaySpider, **spider_args)

process.start()
