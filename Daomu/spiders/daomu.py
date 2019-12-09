# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    #二级页面解析函数
    def parse(self, response):
        li_list=response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for li in li_list:
            item=DaomuItem()
            item['title']=li.xpath('./text()').get()
            link=li.xpath('./@href').get()
            #把link 交给调度器
            yield scrapy.Request(
                url=link,
                #不同解析函数 间传递数据
                meta={'item':item},
                callback=self.parse_two_page
            )

    def parse_two_page(self,response):
        #接收item
        item=response.meta['item']
        article_list=response.xpath('//article[@class="excerpt excerpt-c3"]/a')
        for art in article_list:
            #不能对item['name']赋值,赋值过快,导致只赋值到最后一个
            name=art.xpath('./text()').get()
            link=art.xpath('./@href').get()
            yield scrapy.Request(
                url=link,
                meta={'item':item,'name':name},
                callback=self.parse_three_page
            )

    def parse_three_page(self,response):
        #接收item,name
        item=response.meta['item']
        name=response.meta['name']
        item['name']=name
        content_list=response.xpath('/html/body/section/div[1]/div/article/p/text()').extract()
        item['content']='\n'.join(content_list)

        yield item





