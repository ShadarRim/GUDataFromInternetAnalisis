# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Compose

def clear_desc(values):
    data = {}
    for _ in range(len(values) // 2):
        data[values.pop()] = clear_pop(values.pop())
    return data

def clear_pop(val):
    return val.replace('\n', '').strip()

def to_int(val):
    if val[0].isdigit():
        return int(val[0])
    else:
        return int(''.join(val[0].split(' ')))

class LmItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(to_int), output_processor=TakeFirst())
    cur = scrapy.Field(output_processor=TakeFirst())
    unic_photo = scrapy.Field(output_processor=Identity())
    pict = scrapy.Field(output_processor=Identity())
    art = scrapy.Field(output_processor=Identity())
    unic_pict = scrapy.Field()
    params_dict = scrapy.Field(input_processor=Identity())
    params = scrapy.Field(input_processor=Compose(clear_desc), output_processor=TakeFirst())

