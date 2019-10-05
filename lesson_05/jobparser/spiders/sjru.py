# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

from jobparser.spiders.str_m import list_to_str

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/voditel.html?geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback = self.parse)
        vacancy = response.css('div.f-test-vacancy-item a::attr(href)').extract()       
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = list_to_str( response.xpath('//h1[contains(@class,"_3mfro rFbjy s1nFK _2JVkc")]//text()').extract() )
        salary = list_to_str( response.xpath('//span[contains(@class,"_3mfro _2Wp8I ZON4b PlM3e _2JVkc")]//text()').extract() )
        company = list_to_str( response.xpath('//h2[contains(@class,"_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI")]//text()').extract() )
        yield JobparserItem(name=name, salary=salary, link=response.url, company=company)
