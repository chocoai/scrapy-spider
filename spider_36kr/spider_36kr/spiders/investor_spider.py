# -*- coding: utf-8 -*-

import scrapy
import simplejson as json
from spider_36kr.items import InvestorItem, StartupItem, WorkItem, InvestmentItem


class InvestorSpider(scrapy.Spider):
    name            = "investor"
    start_urls      = ['https://rong.36kr.com/api/organization/investor']
    investor_id     = 20000
    startup_id      = 0
    work_id         = 0
    investment_id   = 0

    def parse(self, response):
        data = json.loads(response.body)['data']
        pages = data['totalPages']
        for it in self.parse_page(response):
            yield it

        for i in range(1, pages):
            yield scrapy.Request('https://rong.36kr.com/api/organization/investor?page=%d' % (i + 1), callback = self.parse_page)

    def parse_page(self, response):
        data = json.loads(response.body)['data']
        for investor in data['data']:
            self.investor_id += 1
            src_id = investor['user']['id']

            item                    = InvestorItem()
            item['id']              = self.investor_id
            item['src_id']          = src_id
            item['src']             = '36kr'
            item['name']            = investor['user']['name']
            item['intro']           = investor['user'].get('intro', '')
            item['weibo']           = investor['user'].get('weibo', '')
            item['weixin']          = investor['user'].get('weixin', '')
            item['linkedin']        = investor['user'].get('linkedin', '')
            item['focusIntustry']   = ','.join(investor['user'].get('focusIntustry', {}).keys())
            item['investCount']     = investor['investComCount']
            item['investPhases']    = ','.join(investor.get('investPhases', []))

            request = scrapy.Request('https://rong.36kr.com/api/user/%d/basic' % src_id, callback = self.parse_basic)
            request.meta['item'] = item
            yield request


    def parse_basic(self, response):
        data = json.loads(response.body)['data']

        item                        = response.meta['item']
        item['school']              = ','.join(data.get('school', []))
        settings                    = data.get('investorSettings', {})
        item['investorSettings']    = json.dumps(settings)
        item['invest_lmt_person']   = settings
        item['invest_lmt_org']      = settings
        item['country']             = data.get('country', '')
        item['city']                = data.get('city', '')

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/company' % item['src_id'], callback = self.parse_startup)
        request.meta['item'] = item
        yield request

    def parse_startup(self, response):
        data = json.loads(response.body)['data']
        item = response.meta['item']
        item['startups'] = []

        for startup in data['expList']:
            self.startup_id += 1

            subitem                 = StartupItem()
            subitem['id']           = self.startup_id
            subitem['investor_id']  = item['id']
            subitem['brief']        = startup.get('brief', '')
            subitem['startDate']    = startup.get('startDate', None)
            subitem['endDate']      = startup.get('endDate', None)
            subitem['kr_group_id']  = startup.get('groupId', 0)
            subitem['groupName']    = startup.get('groupName', '')
            subitem['isCurrent']    = startup.get('isCurrent', False)
            subitem['position']     = startup.get('positionString', '')
            item['startups'].append(subitem)

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/work' % item['src_id'], callback = self.parse_work)
        request.meta['item'] = item
        yield request

    def parse_work(self, response):
        data = json.loads(response.body)['data']
        item = response.meta['item']
        item['works'] = []

        for work in data['expList']:
            self.work_id += 1

            subitem                 = WorkItem()
            subitem['id']           = self.work_id
            subitem['investor_id']  = item['id']
            subitem['brief']        = work.get('brief', '')
            subitem['startDate']    = work.get('startDate', None)
            subitem['endDate']      = work.get('endDate', None)
            subitem['kr_group_id']  = work.get('groupId', 0)
            subitem['groupName']    = work.get('groupName', '')
            subitem['isCurrent']    = work.get('isCurrent', False)
            subitem['position']     = work.get('positionString', '')
            item['works'].append(subitem)

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/past-investment' % item['src_id'], callback = self.parse_investment)
        request.meta['item'] = item
        yield request

    def parse_investment(self, response):
        data = json.loads(response.body)['data']
        item = response.meta['item']
        item['investments'] = []

        for investment in data['data']:
            self.investment_id += 1

            subitem                 = InvestmentItem()
            subitem['id']           = self.investment_id
            subitem['investor_id']  = item['id']
            subitem['kr_group_id']  = investment.get('cid', 0)
            subitem['name']         = investment.get('name', '')
            subitem['brief']        = investment.get('brief', '')
            subitem['industry']     = investment.get('industry', '')
            subitem['latestPhase']  = investment.get('latestPhase', '')
            if 'details' in investment and len(investment['details']) > 0:
                subitem['investDate']   = investment['details'][0].get('investDate', None)
                subitem['phase']        = investment['details'][0].get('phase', '')
                subitem['amount']       = investment['details'][0].get('financeAmount', '')
                subitem['amountUnit']   = investment['details'][0].get('financeAmountUnit', '')
                if 'otherParticipants' in investment['details'][0]:
                    tmp = []
                    for i in investment['details'][0]['otherParticipants']:
                        tmp.append(i['name'])
                    subitem['participant'] = ','.join(tmp)
                else:
                    subitem['participant']  = ''

            item['investments'].append(subitem)

        yield item

