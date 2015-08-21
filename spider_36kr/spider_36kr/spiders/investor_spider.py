# -*- coding: utf-8 -*-

import scrapy
import simplejson as json
from spider_36kr.items import InvestorItem, CompanyItem, WorkItem, InvestmentItem


class InvestorSpider(scrapy.Spider):
    name            = "investor"
    start_urls      = ['https://rong.36kr.com/api/organization/investor']
    result          = {}
    investor_id     = 0
    company_id      = 0
    work_id         = 0
    investment_id   = 0

    def parse(self, response):
        data = json.loads(response.body)['data']
        pages = data['totalPages']
        self.parse_page(response)

        for i in range(1, pages):
            yield scrapy.Request('https://rong.36kr.com/api/organization/investor?page=%d' % (i + 1), callback = self.parse_page)

    def parse_page(self, response):
        data = json.loads(response.body)['data']
        for investor in data['data']:
            self.investor_id += 1
            kr_id = investor['user']['id']

            item                    = InvestorItem()
            item['id']              = self.investor_id
            item['kr_id']           = kr_id
            item['name']            = investor['user']['name']
            item['intro']           = investor['user'].get('intro', '')
            item['weibo']           = investor['user'].get('weibo', '')
            item['weixin']          = investor['user'].get('weixin', '')
            item['linkedin']        = investor['user'].get('linkedin', '')
            item['focusIntustry']   = ','.join(investor['user'].get('focusIntustry', {}).keys())
            item['investCount']     = investor['investComCount']
            item['investPhases']    = ','.join(investor.get('investPhases', []))
            item['country']         = investor.get('country', '') # TODO
            item['city']            = investor.get('city', '') #TODO

            request = scrapy.Request('https://rong.36kr.com/api/user/%d/basic' % kr_id, callback = self.parse_basic)
            request.meta['item'] = item
            yield request


    def parse_basic(self, response):
        data = json.loads(response.body)['data']
        item = response.meta['item']
        item['school'] = ','.join(data.get('school', []))
        item['investorSettings'] = json.dumps(data.get('investorSettings', {}))

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/company' % item['kr_id'], callback = self.parse_company)
        request.meta['item'] = item
        yield request

    def parse_company(self, response):
        data = json.loads(response.body)['data']
        item = response.meta['item']
        item['companys'] = []

        for company in data['expList']:
            self.company_id += 1

            subitem                 = CompanyItem()
            subitem['id']           = self.company_id
            subitem['investor_id']  = item['id']
            subitem['kr_id']        = item['kr_id']
            subitem['brief']        = company.get('brief', '')
            subitem['startDate']    = company.get('startDate', None)
            subitem['endDate']      = company.get('endDate', None)
            subitem['kr_group_id']  = company.get('groupId', 0)
            subitem['groupName']    = company.get('groupName', '')
            subitem['isCurrent']    = company.get('isCurrent', False)
            subitem['position']     = company.get('positionString', '')
            item['companys'].append(subitem)

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/work' % item['kr_id'], callback = self.parse_work)
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
            subitem['kr_id']        = item['kr_id']
            subitem['brief']        = work.get('brief', '')
            subitem['startDate']    = work.get('startDate', None)
            subitem['endDate']      = work.get('endDate', None)
            subitem['kr_group_id']  = work.get('groupId', 0)
            subitem['groupName']    = work.get('groupName', '')
            subitem['isCurrent']    = work.get('isCurrent', False)
            subitem['position']     = work.get('positionString', '')
            item['works'].append(subitem)

        request = scrapy.Request('https://rong.36kr.com/api/user/%d/past-investment' % item['kr_id'], callback = self.parse_investment)
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
            subitem['kr_id']        = item['kr_id']
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

