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
    host_chengjiao = "https://hz.lianjia.com/chengjiao/"
    start_urls = ["西湖", "江干", "拱墅", "上城", "下城", "滨江", "余杭", "萧山", "下沙"]
    crawl_regions = set(start_urls)
    finish_regions = set(start_urls)

    # 设置区域
    def start_requests(self):
        while self.crawl_regions.__len__():
            region = self.crawl_regions.pop()
            self.finish_regions.add(region)
            url_region = self.host_chengjiao + ''.join(lazy_pinyin(region))
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
                if sub_match:
                    items["subway"] = sub_match.group(1)
                if deal_date_match:
                    items["deal_date"] = deal_date_match.group(1)
                yield Request(url=url, meta={"item": items}, callback=self.parse_third)
        page_content = selector.xpath("//div[@class='page-box house-lst-page-box']").extract()
        if page_content is not None and items["plies"] == 1:
            total_page = re.compile('"totalPage":(.*?),').search(page_content[0]).group(1)
            for page in range(1, int(total_page)):
                items["plies"] = 0
                url_region = self.host_chengjiao + ''.join(lazy_pinyin(items["regions"]))
                page_str = "pg"+str(page)
                block_url = urljoin(url_region,page_str)
                yield Request(url=block_url, meta={"item": items}, callback=self.parse_second)

    def parse_third(self, response):
        url = response.url
        items = response.meta["item"]
        selector = Selector(response)
        items["href"] = url
        items["name"] = selector.xpath("//div[@class='wrapper']/text()").extract()[0]
        items["style"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[1]/text()').extract()[0]
        items["area"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[3]/text()').extract()[0]
        items["orientation"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[7]/text()').extract()[0]
        items["decoration_situation"] = selector.xpath(
                '//*[@id="introduction"]/div/div[1]/div[2]/ul/li[9]/text()').extract()[0]
        items["floor"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[2]/text()').extract()[0]  # 楼层
        items["year"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[8]/text()').extract()[0]  # 年份
        items["unit_price"] = selector.xpath('//div[@class="price"]/b/text()').extract()[0]  # 单价
        items["total_price"] = selector.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[0]  # 总价1爬取的价格
        items["elevator"] = selector.xpath('//*[@id="introduction"]/div/div[1]/div[2]/ul/li[14]/text()').extract()[0]  # 电梯
        items["deal_time"] = selector.xpath('//div[@class="msg"]/span[2]/label/text()').extract()[0]  # 成交周期
        items["quote_time"] = selector.xpath(
                '//*[@id="introduction"]/div/div[2]/div[2]/ul/li[3]/text()').extract()[0]  # 挂牌时间
        items["housing_use"] = selector.xpath(
                '//*[@id="introduction"]/div/div[2]/div[2]/ul/li[4]/text()').extract()[0]  # 房屋用途
        items["owner_ship"] = selector.xpath(
                '//*[@id="introduction"]/div/div[2]/div[2]/ul/li[6]/text()').extract()[0]  # 产权所属
        items["owner_time"] = selector.xpath(
                '//*[@id="introduction"]/div/div[1]/div[2]/ul/li[13]/text()').extract()[0]  # 产权年限
        items["deal_ship"] = selector.xpath(
                '//*[@id="introduction"]/div/div[2]/div[2]/ul/li[2]/text()').extract()  # 交易权属
