# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class MaoyanPipeline(object):

    def process_item(self, item, spider):

        with open(r'E:/downloadfile/maoyan.txt', 'a') as f:
            text = item['title'] + ',' + item['actor'] + ',' + \
                   item['time'] + ',' + item['score'] + '\n'
            f.write(text)

        return item


class MongoPipline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.port = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        info = dict(item)
        print(info)
        self.port.insert(info)
        return item


