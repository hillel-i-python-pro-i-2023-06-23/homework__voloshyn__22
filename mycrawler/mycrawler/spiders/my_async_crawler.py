import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mycrawler.items import MyCrawlerItem

class MyAsyncCrawlerSpider(CrawlSpider):
    name = 'my_async_crawler'
    allowed_domains = ['scrapy.org']
    start_urls = ['https://scrapy.org']

    rules = (
        Rule(LinkExtractor(allow=('/',)), callback='parse_start_page', follow=True),
    )

    async def parse_start_page(self, response):
        item = MyCrawlerItem()
        item['url'] = response.url
        yield item
