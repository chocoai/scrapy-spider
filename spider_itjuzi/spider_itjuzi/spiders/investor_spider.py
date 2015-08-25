# -*- coding: utf-8 -*-

import scrapy
from spider_itjuzi.items import InvestorItem, InvestmentItem
from bs4 import BeautifulSoup


class InvestorSpider(scrapy.Spider):
    name            = "investor"
    start_urls      = ['http://itjuzi.com/investor']
    investor_id     = 0
    investment_id   = 0

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        for a in soup.select('#page-content .person-list a.media-tit'):
            link = a.get('href')
            yield scrapy.Request(link, callback = self.parse_investor)

        for a in soup.select('#page-content .next a'):
            text = a.get_text()
            if '下一页'.decode('utf-8') in text:
                yield scrapy.Request(a.get('href'), callback = self.parse)

    def parse_investor(self, response):
        self.investor_id += 1
        soup = BeautifulSoup(response.body, 'html.parser')

        item                = InvestorItem()
        item['id']          = self.investor_id
        item['itjuzi_id']   = response.url.split('/')[-1]
        item['name']        = soup.select_one('.public-info a').string.strip()

        for li in soup.select('.detail-info li'):
            title, content = [x.strip() for x in li.get_text().split(':', 1)]
            if '职位'.decode('utf-8') in title:
                item['position']= content
            elif '微博'.decode('utf-8') in title:
                item['weibo']   = content
            elif '介绍'.decode('utf-8') in title:
                item['brief']   = content
            elif '地点'.decode('utf-8') in title:
                item['address'] = content
            elif '工作'.decode('utf-8') in title:
                item['company'] = content
            elif '教育'.decode('utf-8') in title:
                item['school']  = content
            elif '投资领域'.decode('utf-8') in title:
                item['intustry']= content

        item['investments'] = []
        for div in soup.select('#company-similar .media'):
            self.investment_id += 1

            investment                  = InvestmentItem()
            investment['id']            = self.investment_id
            investment['investor_id']   = self.investor_id
            investment['itjuzi_id']     = item['itjuzi_id']
            investment['name']          = div.h4.get_text()
            investment['company_url']   = div.h4.a.get('href')
            investment['investDate'], investment['phase'], investment['amount'] \
                = [x.get_text().strip() for x in div.select('p')]
            item['investments'].append(investment)

        yield item

