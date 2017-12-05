# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector

from craw_pengpainews.items import CrawPengpainewsItem


class NewsSpider(Spider):
    name = 'increment'
    allowed_domains = ['www.thepaper.cn']
    start_urls = ['http://www.thepaper.cn/list_25433']

    def parse(self, response):
        sel = Selector(response)
        all_li = sel.xpath('//*[@class="news_li"]')
        print(all_li.__len__())
        # items = []
        if all_li:
            for li in all_li:
                item = CrawPengpainewsItem()
                url = li.xpath('div/a/@href').extract()
                img_url = li.xpath('div/a/img/@src').extract()
                title = li.xpath('h2/a/text()').extract()
                praise_num = li.xpath('div[2]/span[2]/text()').extract()

                item['title'] = title
                item['link'] = 'http://www.thepaper.cn/'+str(url[0])
                if praise_num:
                    item['praise_num'] = praise_num
                else:
                    item['praise_num'] = 0
                item['url'] = img_url
                yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse_detail,
                                     dont_filter=True)

    def parse_detail(self, response):
            item = response.meta['item']
            date = response.xpath('//*[@class="news_about"]/p[2]/text()').extract()[0]
            item['date'] = re.sub(r"[\*,\t,\n,\+]","",date)
            content = response.xpath('//*[@class="news_txt"]/text()').extract()
            item['content'] = self.getContent(content)[1:1800]

            yield item

    @staticmethod
    def getContent(content):
        co = ''
        for i in range(len(content)):
            co += content[i]
        return co