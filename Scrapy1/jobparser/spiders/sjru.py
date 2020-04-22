# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, keyword):
        self.start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={keyword}']

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@rel='next']/@href").extract_first()

        vacancy_links = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page, callback=self.parse)

    def vacancy_parce(self, response: HtmlResponse):
        name1 = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/@text").extract_first()
        salary1 = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        link1 = response.url
        src = "sj.ru"
        yield JobparserItem(name=name1, salary=salary1, link=link1, src=src)
