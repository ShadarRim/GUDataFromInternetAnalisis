# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LmPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lmdb

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LmPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['unic_photo']:
            unic_photos_count = len(item['unic_photo'])
            item['unic_pict'] = []
            for i in range(0, len(item['pict']), int(len(item['pict']) / unic_photos_count)):
                item['unic_pict'].append(item['pict'][i])
            for img in item['unic_pict']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results[0]:
            item['unic_pict'] = [itm[1] for itm in results if itm[0]]
        return item
