# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    src = scrapy.Field()
    s_min = scrapy.Field()
    s_max = scrapy.Field()
    s_cur = scrapy.Field()
