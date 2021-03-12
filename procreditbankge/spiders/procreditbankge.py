import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from procreditbankge.items import Article


class ProcreditbankgeSpider(scrapy.Spider):
    name = 'procreditbankge'
    start_urls = ['https://www.procreditbank.ge/ge/news-archive']

    def parse(self, response):
        links = response.xpath('//a[@class="news-readmore"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//span[@class="block-title-text without-arrow"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="page-head-dates"]//text()').get()
        if date:
            date = " ".join(date.strip().split()[1:])

        content = response.xpath('//div[@class="deposit-inner-block"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
