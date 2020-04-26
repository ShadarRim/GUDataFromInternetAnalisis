# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LmItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    cur = scrapy.Field()
    unic_photo = scrapy.Field()
    pict = scrapy.Field()
    unic_pict = scrapy.Field()
    params_name = scrapy.Field()
    params_value = scrapy.Field()
    params_dict = scrapy.Field()

