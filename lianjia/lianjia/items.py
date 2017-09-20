# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    regions = Field()  # 区域
    block = Field()  # 街区
    deal_date = Field()  # 成交日期
    href = Field()  # 链接
    name = Field()  # 名称
    style = Field()  # 房屋户型
    area = Field()  # 面积
    orientation = Field()  # 房屋朝向
    decoration_situation = Field()  # 装修情况
    floor = Field()  # 楼层
    year = Field()  # 年份
    unit_price = Field()  # 单价
    total_price = Field()  # 总价1爬取的价格
    subway = Field()  # 地铁
    elevator = Field()  # 电梯
    deal_time = Field()  # 成交周期
    quote_time = Field()  # 挂牌时间
    housing_use = Field()  # 房屋用途
    owner_ship = Field()  # 产权所属
    owner_time = Field()  # 产权年限
    deal_ship = Field()  # 交易权属

    plies = Field()  # 传递url用
