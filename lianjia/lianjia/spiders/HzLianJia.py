import re
from urllib.parse import urljoin

from lianjia.items import LianjiaItem
from pypinyin import lazy_pinyin
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider


class HzLianJia(CrawlSpider):
    name = "HzLianJia"
    host = "http://hz.lianjia.com"
    start_urls = ["西湖", "江干", "拱墅", "上城", "下城", "滨江", "余杭", "萧山", "下沙"]
    crawl_regions = set(start_urls)
    finish_regions = set(start_urls)

    # 设置区域
    def start_requests(self):
        while self.crawl_regions.__len__():
            region = self.crawl_regions.pop()
            self.finish_regions.add(region)
            url_region = "https://hz.lianjia.com/chengjiao/" + ''.join(lazy_pinyin(region))
            lianjiaItems = LianjiaItem()
            lianjiaItems["regions"] = region
            yield Request(url=url_region, meta={"item": lianjiaItems}, callback=self.parse_first)

    # 设置街区
    def parse_first(self, response):
        url = response.url
        items = response.meta["item"]
        selector = Selector(response)
        block_url_list = selector.xpath('//div[@class="position"]/dl[2]/dd/div/div[2]/a/@href').extract()
        block_name_list = selector.xpath('//div[@class="position"]/dl[2]/dd/div/div[2]/a/text()').extract()
        while block_url_list:
            block_url = urljoin(url, block_url_list.pop())
            while block_name_list:
                items["block"] = block_name_list.pop()  # 应该做一个判断
                items["plies"] = 1
                yield Request(url=block_url, meta={"item": items}, callback=self.parse_second)

    def parse_second(self, response):
        url = response.url
        selector = Selector(response)
        items = response.meta["item"]
        list_content = selector.xpath("//div[@class='info']").extract()
        pattern_href = re.compile(u'href="(.*?)"')
        pattern_subway = re.compile(u'<span class="dealHouseTxt"><span>(.*?)</span></span>')
        pattern_deal_date = re.compile(u'<div class="dealDate">(.*?)</div>')
        while list_content:
            content = list_content.pop()
            url_search = pattern_href.search(content)
            if url_search:
                url = url_search.group(1)
                sub_match = pattern_subway.search(content)
                deal_date_match = pattern_deal_date.search(content)
                items["subway"] = sub_match.group(1)
                items["deal_date"] = deal_date_match.group(1)
                yield Request(url=url, meta={"item": items}, callback=self.parse_third)
        page_content = selector.xpath("//div[@class='page-box house-lst-page-box']").extract()
        if page_content is not None and items["plies"] == 1:
            for total_page in page_content:
                total_page = re.compile('"totalPage":(.*?),').search(page_content[0]).group(1)
                for page in range(1, int(total_page)):
                    items["plies"] = 0
                    yield Request(url=block_url, meta={"item": items}, callback=self.parse_second)

    def parse_third(self, response):
        url = response.url
        items = response.meta["item"]
        items["href"] = url  # 链接
        name = Field()  # 名称
        style = Field()  # 房屋户型
        area = Field()  # 面积
        orientation = Field()  # 房屋朝向
        decoration_situation = Field()  # 装修情况
        floor = Field()  # 楼层
        year = Field()  # 年份
        sign_time = Field()  # 注册时间
        unit_price = Field()  # 单价
        total_price_first = Field()  # 总价1爬取的价格
        total_price_second = Field()  # 总价2=area*unit_price
        house_property = Field()  # 房产类关于房产时间的
        school = Field()  # 学校
        subway = Field()  # 地铁
        elevator = Field()  # 电梯
        deal_time = Field()  # 成交周期
        quote_time = Field()  # 挂牌时间
        housing_use = Field()  # 房屋用途
        owner_ship = Field()  # 产权所属
        owner_time = Field()  # 产权年限
        deal_ship = Field()  # 交易权属