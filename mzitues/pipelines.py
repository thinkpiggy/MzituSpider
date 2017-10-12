# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MzituesPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        super().process_item(item, spider)

    def get_media_requests(self, item, info):
        return [Request(x, headers={'Referer': item.get('url'),'Warning': item.get('category') + '/' + item.get('title') + '/' + os.path.split(x)[1]}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        return 'full/%s' % (request.headers['Warning'].decode())
    #     path = os.path.split()[0]
    #     if os.path.exists(path) is False:
    #         os.mkdir(path)
    #     return 'full/%s.jpg' % (request.headers.Warning)
