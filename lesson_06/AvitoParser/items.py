# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def photo_cleaner(values):
    if values[:2] == '//':
        return 'http:' + values
    return values

def params_extractor(params):
    temp = [p.strip() for p in params]
    temp = [p.replace('\xa0', '') for p in temp if p]
    return zip(temp[0::2], temp[1::2])

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor = TakeFirst())
    photos = scrapy.Field(input_processor = MapCompose(photo_cleaner))
    params = scrapy.Field(input_processor = params_extractor)
    pass
