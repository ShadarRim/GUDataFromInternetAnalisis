# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lm.items import LmItem

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
        name = response.xpath("//h1[@slot='title']/text()").extract_first()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()").extract_first()
        cur = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()").extract_first()
        unic_photo = response.xpath("//picture[@slot='pictures']").extract()
        pict = response.xpath("//picture[@slot='pictures']/source/@srcset").extract()
        params_name = response.xpath("//dt[@class='def-list__term']/text()").extract()
        params_value = response.xpath("//dd[@class='def-list__definition']/text()").extract()
        #big_photo_count = len(response.xpath("//picture[@slot='pictures']").extract())
        #pict = response.xpath("//picture[@slot='pictures']/source/@srcset").extract()
        #pict_to_extract = []
        #for i in range(0,len(pict),int(len(pict)/big_photo_count))
        #    pict_to_extract.append(pict[i])

        yield LmItem(name=name, price=price, cur=cur, unic_photo=unic_photo, pict=pict, params_name=params_name, params_value=params_value)
