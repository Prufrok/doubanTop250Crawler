import logging
from re import sub
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from doubanTop250Crawler.items import DoubanItem

class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250?start=0']
    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,
    }
    count = 0

    rules = (
        # By default if no callback is given, `follow` is true
        Rule(LinkExtractor(restrict_css='span.next a')),
        # otherwise, `follow` is false
        Rule(LinkExtractor(allow=r'/subject/\d+/'), callback='parse_item'),
    )

    def parse_item(self, response):
        def get_rate():
            rate = response.css('strong[property="v:average"]::text').get()
            if rate:
                return float(rate)
            else:
                return None

        book = DoubanItem()

        book['title'] = response.css('[property$="itemreviewed"]::text').get()
        # book['title'] = response.xpath('//*[contains(@property, "itemreviewed")]/text()').get()

        book['url'] = response.url

        book['img_url'] = response.css('#mainpic img::attr(src)').get()
        # book['img_url'] = response.xpath('//*[@id="mainpic"]//img/@src').get()

        # book['author'] = '；'.join(response.css('a[href*="/author/"]::text').getall())
        book['author'] = sub(
            '[\n ]', '',
            '；'.join(response.xpath(
                '//a[contains(@href, "/author/") or contains(@href, "/search/")]/text()').getall())
        )

        book['rate'] = get_rate()

        book['votes_num'] = int(response.css(
            '[property$="votes"]::text').get())

        book['comments_num'] = response.css(
            '.mod-hd span.pl a::text').re('\d+')[0]

        self.count += 1
        logging.warning(f'Book crawled: {self.count}/250')

        return book
