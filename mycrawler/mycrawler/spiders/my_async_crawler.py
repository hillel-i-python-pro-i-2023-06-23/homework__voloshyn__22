import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mycrawler.items import MyCrawlerItem
import time

class MyAsyncCrawlerSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(MyAsyncCrawlerSpider, self).__init__(*args, **kwargs)
        self.visited_urls = set()  # Множество для отслеживания посещенных URL
        self.items_processed = 0
        self.start_time = time.time()

        # Считываем allowed_domains из файла
        with open('domains.txt', 'r') as domains_file:
            self.allowed_domains = [line.strip() for line in domains_file]

        # Считываем start_urls из файла
        with open('start_urls.txt', 'r') as start_urls_file:
            self.start_urls = [line.strip() for line in start_urls_file]

    name = 'my_async_crawler'
    rules = (
        Rule(LinkExtractor(allow=('/')), callback='parse_start_page', follow=True),
    )

    async def parse_start_page(self, response):
        item = MyCrawlerItem()
        item['url'] = response.url
        if response.url not in self.visited_urls:  # Проверяем, не посещали ли уже этот URL
            self.visited_urls.add(response.url)  # Добавляем URL в множество посещенных
            yield item
            self.items_processed += 1

    def closed(self, reason):
        end_time = time.time()
        elapsed_time = end_time - self.start_time  # Время, затраченное на краулинг
        crawl_speed = self.items_processed / elapsed_time  # Рассчитываем скорость
        print(f'Crawling speed: {crawl_speed:.2f} items/second')
