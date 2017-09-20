# -*- coding: utf-8 -*-
from imp import reload

import pymysql
import sys
from lianjia.items import LianjiaItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lianjia import settings


class LianjiaPipeline(object):
    def open_spider(self, spider):
        # default_encoding = 'utf-8'
        # reload(sys)
        # sys.setdefaultencoding(default_encoding)
        host = settings.MYSQL_HOST
        name = settings.MYSQL_NAME
        password = settings.MYSQL_PASSWORD
        db_name = settings.MYSQL_DBNAME
        self.db = pymysql.connect(host, name, password, db_name,charset="utf8")
        # self.db.set_character_set('utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if item.__class__ == LianjiaItem:
            for key, value in item.items():
                if isinstance(item[key], str):
                    item[key] = value.strip()
            insert_sql = "INSERT INTO " + settings.MYSQL_TABLE + "(REGIONS, BLOCK, DEAL_DATE, HREF, NAME, STYLE, AREA, ORIENTATION, DECORATION_SITUATION, FLOOR, YEAR, UNIT_PRICE, TOTAL_PRICE, SUBWAY, ELEVATOR, DEAL_TIME, QUOTE_TIME, HOUSING_USE, OWNER_SHIP, OWNER_TIME,DEAL_SHIP) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                item['regions'], item['block'], item['deal_date'], item['href'], item['name'], item['style'],
                item['area'], item['orientation'], item["decoration_situation"], item["floor"], item["year"],
                item["unit_price"], item["total_price"], item["subway"], item["elevator"], item["deal_time"],
                item["quote_time"], item["housing_use"], item["owner_ship"], item["owner_time"], item["deal_ship"])
            self.cursor.execute(insert_sql)  # 执行sql语句
            self.db.commit()  # 提交到数据库，insert和updata语句必须执行这句
            return item

    def spier_close(self, spder):
        self.db.close()
