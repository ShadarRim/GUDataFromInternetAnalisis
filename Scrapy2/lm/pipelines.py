# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class LmPipeline(object):
    def process_item(self, item, spider):
        return item

class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        pass

    def item_completed(self, results, item, info):
        return item

'''
        print('hi')
        a = 5

        if item['unic_photo']:
            unic_photos_count = len(item['unic_photo'])
            item['unic_pict'] = []
            for i in range(0, len(item['pict']), int(len(item['pict'])/unic_photos_count)):
                item['unic_pict'].append(item['pict'][i])
            for img in item['unic_pict']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
'''