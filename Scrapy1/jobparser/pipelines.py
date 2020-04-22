# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pprint import pprint
import numpy as np

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy312

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            item['s_min'] = None
            item['s_max'] = None
            item['s_cur'] = None
            if 'от ' in item['salary'] and ' до ' in item['salary']:
                item['s_min'] = item['salary'][1].replace('\xa0', '')
                item['s_max'] = item['salary'][3].replace('\xa0', '')
                item['s_cur'] = item['salary'][5]
            elif 'от ' in item['salary'] and ' до ' not in item['salary']:
                item['s_min'] = item['salary'][1].replace('\xa0', '')
                item['s_cur'] = item['salary'][3]

        if spider.name == 'sjru':
            item['s_min'] = ''
            item['s_max'] = ''
            item['s_cur'] = None
            if 'от' in item['salary']:
                #print('here-1')
                sub_list = item['salary'][2].split('\xa0')
                for i in range(len(sub_list)-1):
                    item['s_min'] += sub_list[i]
                item['s_cur'] = sub_list[-1]
            elif 'до' in item['salary']:
                sub_list = item['salary'][2].split('\xa0')
                for i in range(len(sub_list)-1):
                    item['s_max'] += sub_list[i]
                item['s_cur'] = sub_list[-1]
            elif 'По договорённости' not in item['salary']:
                item['s_min'] = item['salary'][0].replace('\xa0', '')
                item['s_max'] = item['salary'][1].replace('\xa0', '')
                item['s_cur'] = item['salary'][3]
            item['s_min'] = None if item['s_min'] == '' else item['s_min']
            item['s_max'] = None if item['s_max'] == '' else item['s_max']

        if not collection.count_documents(item):
            collection.insert_one(item)

        return item
