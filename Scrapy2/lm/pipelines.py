# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from urllib.parse import urlparse
import os
from pprint import pprint

class LmPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lmdb

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        to_collect = {}
        to_collect['name'] = item['name']
        to_collect['unic_pict'] = item['unic_pict']
        to_collect['params'] = item['params']
        to_collect['price'] = item['price']
        to_collect['cur'] = item['cur']

        collection.insert_one(to_collect)
        return item

class LmPhotosPipeline(ImagesPipeline):

    item_art = ""

    def get_media_requests(self, item, info):
        if item['unic_photo']:
            unic_photos_count = len(item['unic_photo'])
            item['unic_pict'] = []
            self.item_art = item['art'][0]
            for i in range(0, len(item['pict']), int(len(item['pict']) / unic_photos_count)):
                item['unic_pict'].append(item['pict'][i])
            for img in item['unic_pict']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        #вы итак знаете, что здесь что-то с асинхронностью)
        return f'{info.spider.name}/' + f"{self.item_art}/" + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results[0]:
            item['unic_pict'] = [itm[1] for itm in results if itm[0]]
        return item
