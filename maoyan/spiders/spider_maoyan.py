import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from maoyan.items import MaoyanItem

class SpiderMaoyan(scrapy.Spider):
    name = 'maoyan'

    start_urls = [
        'http://maoyan.com/board/4?offset=0'
    ]

    def parse(self, response):
        item = MaoyanItem()
        selector = Selector(response)
        infos = selector.xpath('//dl[@class="board-wrapper"]/dd')
        for info in infos:
            title = info.xpath('div/div/div[1]/p[1]/a/text()').extract()[0]
            actor = info.xpath('div/div/div[1]/p[2]/text()').extract()[0].strip()
            time = info.xpath('div/div/div[1]/p[3]/text()').extract()[0]
            score = info.xpath('div/div/div[2]/p/i[1]/text()').extract()[0] + \
                    info.xpath('div/div/div[2]/p/i[2]/text()').extract()[0]

            item['title'] = title
            item['actor'] = actor
            item['time'] = time
            item['score'] = score

            yield item

        urls = ['http://maoyan.com/board/4?offset={}'.format(str(i)) for i in range(10, 100, 10)]
        for url in urls:
            yield Request(url, callback=self.parse)