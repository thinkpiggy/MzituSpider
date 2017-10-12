# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.loader import ItemLoader

from mzitues.items import MzituesItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']

    def start_requests(self):
        # 从首页开始抓取,支持指定专题
        start_url = 'http://www.mzitu.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            start_url += 'tag/' + tag
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):

        # 导航翻页
        next_page = response.xpath("//a[@class='next page-numbers']/@href")
        if next_page is not None:
            yield scrapy.Request(next_page.extract_first(), self.parse)

        # 帖子
        for post in response.xpath("//div[@class='postlist']/ul/li/a/@href"):
            yield scrapy.Request(post.extract(), self.parse_post)

    def parse_post(self, response):
        content = response.xpath("//div[@class='content']")[0]
        item = MzituesItem()
        item['url'] = response.url
        item['title'] = content.xpath("h2/text()").extract_first()
        item['category'] = content.xpath("div[@class='main-meta']/span/a/text()").extract_first()
        item['image_urls'] = self.build_image_urls(content)
        yield item

    def build_image_urls(self, content):
        image_url = content.xpath("div[@class='main-image']/p/a/img/@src").extract_first()
        path, base = os.path.split(image_url)
        name, ext = base.split('.')
        pages = int(content.xpath("div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(), 10)
        image_urls = []
        for page in range(1, pages + 1):
            image_urls.append('%s/%s%02d.%s' % (path, name[:-2], page, ext))
        return image_urls
