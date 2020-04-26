# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lm.items import LmItem
from scrapy.loader import ItemLoader

class LermerSpider(scrapy.Spider):
    name = 'lermer'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, keyword):
        self.start_urls = [f'http://leroymerlin.ru/search/?q={keyword}']

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@rel='next']/@href").extract_first()

        target_links = response.xpath("//div[@class='ui-product-card']/@data-product-url").extract()

        for link in target_links:
            yield response.follow(link, callback=self.pars_target)

        yield response.follow(next_page, callback=self.parse)

    def pars_target(self, response:HtmlResponse):
        print(response.url)
        loader = ItemLoader(item=LmItem(), response=response)
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('cur', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()")
        loader.add_xpath('unic_photo', "//picture[@slot='pictures']")
        loader.add_xpath('pict', "//picture[@slot='pictures']/source/@srcset")
        loader.add_xpath('params', "//dt[@class='def-list__term']/text() | //dd[@class='def-list__definition']/text()")

        yield loader.load_item()

#        name = response.xpath("//h1[@slot='title']/text()").extract_first()
#        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()").extract_first()
#        cur = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()").extract_first()
#        unic_photo = response.xpath("//picture[@slot='pictures']").extract()
#        pict = response.xpath("//picture[@slot='pictures']/source/@srcset").extract()
#        params_name = response.xpath("//dt[@class='def-list__term']/text()").extract()
#        params_value = response.xpath("//dd[@class='def-list__definition']/text()").extract()

#        yield LmItem(name=name, price=price, cur=cur, unic_photo=unic_photo, pict=pict, params_names=params_name, params_values=params_value)
