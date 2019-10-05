# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

from jobparser.spiders.str_m import list_to_str

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://tomsk.hh.ru/search/vacancy?area=113&st=searchVacancy&text=Водитель']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback = self.parse)
        vacancy = response.css('div.vacancy-serp div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = list_to_str( response.xpath('//div[contains(@class,"vacancy-title")]//h1[@class="header"]//text()').extract() )
        salary = list_to_str( response.xpath('//div[contains(@class,"vacancy-title")]/p[@class="vacancy-salary"]/text()').extract_first() )
        company = list_to_str( response.xpath('//a[@class="vacancy-company-name"]/span/text()').extract_first() )
        yield JobparserItem(name=name, salary=salary, link=response.url, company=company)
