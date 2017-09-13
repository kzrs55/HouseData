# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Selector, FormRequest
from scrapy.http.request import Request
from scrapy.spiders import Rule


class LianjiaPipeline(object):
    allowed_domains = ["https://hz.lianjia.com"]
    start_urls = [
        "https://hz.lianjia.com/ershoufang/"
    ]

