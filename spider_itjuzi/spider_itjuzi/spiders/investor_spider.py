# -*- coding: utf-8 -*-

import scrapy
from spider_itjuzi.items import InvestorItem, InvestmentItem, WorkItem
from bs4 import BeautifulSoup


class InvestorSpider(scrapy.Spider):
    name            = "investor"
    start_urls      = ['http://itjuzi.com/investor']
    investor_id     = 10000
    investment_id   = 0
    work_id         = 0

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
        item['src_id']      = response.url.split('/')[-1]
        item['src']         = 'itjuzi'
        item['name']        = soup.select_one('.public-info a').string.strip()
        item['works']       = []
        item['investments'] = []

        for li in soup.select('.detail-info li'):
            title, content = [x.strip() for x in li.get_text().split(':', 1)]
            if '职位'.decode('utf-8') in title:
                item['position']= content
                self.split_position(item, content)
            elif '微博'.decode('utf-8') in title:
                item['weibo']   = content
            elif '介绍'.decode('utf-8') in title:
                item['brief']   = content
            elif '地点'.decode('utf-8') in title:
                item['address'] = content
            elif '工作'.decode('utf-8') in title:
                item['company'] = content
                self.split_company(item, content)
            elif '教育'.decode('utf-8') in title:
                item['school']  = content
            elif '投资领域'.decode('utf-8') in title:
                item['intustry']= content

        for div in soup.select('#company-similar .media'):
            self.investment_id += 1

            investment                  = InvestmentItem()
            investment['id']            = self.investment_id
            investment['investor_id']   = self.investor_id
            investment['name']          = div.h4.get_text()
            investment['company_url']   = div.h4.a.get('href')
            investment['investDate'], investment['phase'], investment['amount'] \
                = [x.get_text().strip() for x in div.select('p')]
            item['investments'].append(investment)

        yield item

    def split_position(self, item, content):
        if not content:
            return

        for val in content.split(','):
            self.work_id += 1

            work                = WorkItem()
            work['id']          = self.work_id
            work['investor_id'] = item['id']
            work['name'], work['position'] = \
                [x.strip() for x in val.strip().split(' ', 1)]
            item['works'].append(work)

    def split_company(self, item, content):
        if not content:
            return

        for val in content.split(','):
            self.work_id += 1

            work                = WorkItem()
            work['id']          = self.work_id
            work['investor_id'] = item['id']
            work['name']        = val
            item['works'].append(work)
