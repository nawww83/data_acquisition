# -*- coding: utf-8 -*-
import scrapy
from AvitoParser.items import AvitoparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/tomsk/avtomobili']

    def parse(self, response: HtmlResponse):
        xp = '//a[@class="item-description-title-link"]/@href'
        ads_links = response.xpath(xp).extract()
        for l in ads_links:
            yield response.follow(l, self.link_parse)

    def link_parse(self, response: HtmlResponse):
        loader = ItemLoader(item = AvitoparserItem(), response = response)
        xp = '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url'
        loader.add_xpath('photos', xp)
        xp = '//h1[@class="title-info-title"]/span/text()'
        loader.add_xpath('name', xp)
        xp = '//div[@class="item-params"]//li[@class="item-params-list-item"]//text()'
        loader.add_xpath('params', xp)
        yield loader.load_item()
'''
        xp = '//h1[@class="title-info-title"]/span/text()'
        name = response.xpath(xp).extract()
        xp = '//div[@class="item-params"]//li[@class="item-params-list-item"]//text()'
        params = response.xpath(xp).extract()
        xp = '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url'
        photos = response.xpath(xp).extract()
        yield AvitoparserItem(name = name, photos = photos, params = params)
'''
