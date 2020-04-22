# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, keyword):
        self.start_urls = [f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={keyword}']

    def parse(self, response:HtmlResponse):
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response: HtmlResponse):
        name1 = response.css("div.vacancy-title h1::text").extract_first()
        salary1 = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        link1 = response.url
        src = "hh.ru"
        yield JobparserItem(name=name1, salary=salary1, link=link1, src=src)
