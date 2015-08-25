# -*- coding: utf-8 -*-

import scrapy
from spider_fellowplus.items import InvestorItem, InvestmentItem, WorkItem, EducationItem, QAItem
from bs4 import BeautifulSoup


class InvestorSpider(scrapy.Spider):
    name            = "investor"
    start_urls      = ['https://fellowplus.com/investors/']
    investor_id     = 0
    education_id    = 0
    work_id         = 0
    investment_id   = 0
    qa_id           = 0

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        for div in soup.select('.user-item'):
            yield scrapy.Request(div.a.get('href'), callback = self.parse_investor)

        a = soup.select('.page-navi .next a')
        if len(a) > 0:
            yield scrapy.Request('https://fellowplus.com%s' % a[0].get('href'), callback = self.parse)

    def parse_investor(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        self.investor_id += 1

        item                = InvestorItem()
        item['id']          = self.investor_id
        item['name']        = soup.select_one('.section-profile h4').get_text()
        item['position']    = soup.select_one('.section-profile .position').get_text()
        item['brief']       = soup.select_one('.section-profile .foudation').get_text()

        for li in soup.select('.block-data li'):
            span = li.span.extract()
            title = li.get_text().strip()
            content = span.strong.get_text()
            if '开始投资'.decode('utf-8') in title:
                item['investStart'] = content
            elif '已投项目'.decode('utf-8') in title:
                item['investCount'] = content
            elif '项目走到下一轮'.decode('utf-8') in title:
                item['investNextPhase'] = content
            elif '成功退出项目'.decode('utf-8') in title:
                item['investQuit'] = content

        for li in soup.select('.investment-style li'):
            title = li.label.get_text()
            content = li.p.get_text()
            if '偏好投资阶段'.decode('utf-8') in title:
                item['investPhases'] = content
            elif '单个项目投资额度'.decode('utf-8') in title:
                item['investLimit'] = content
            elif '计划一年投资项目个数'.decode('utf-8') in title:
                item['investPlan'] = content
            elif '关注领域'.decode('utf-8') in title:
                item['focusIntustry'] = content
            elif '常驻城市'.decode('utf-8') in title:
                item['city'] = content

        item['investments'] = []
        for li in soup.select('.production-list li'):
            self.investment_id += 1

            investment                  = InvestmentItem()
            investment['id']            = self.investment_id
            investment['investor_id']   = item['id']
            investment['name']          = li.select_one('.info-main h4').get_text()
            investment['phase']         = li.select_one('.info-main p').get_text().split('：'.decode('utf-8'), 1)[1]
            investment['brief']         = li.select_one('.intro').get_text()
            item['investments'].append(investment)

        item['educations'] = []
        item['works'] = []
        for div in soup.select('.sub-block'):
            block_title = div.h6.get_text()

            if '教育经历'.decode('utf-8') in block_title:
                for li in div.select('li'):
                    self.education_id += 1

                    education                   = EducationItem()
                    education['id']             = self.education_id
                    education['investor_id']    = item['id']
                    texts = [x.strip() for x in li.h6.get_text().split('&bullet;', 1)]
                    education['school'] = texts[0]
                    if len(texts) >= 2:
                        education['major'] = texts[1]

                    if li.p:
                        texts = [x.strip() for x in li.p.get_text().split('-', 1)]
                        education['startDate'] = texts[0]
                        if len(texts) >= 2:
                            education['endDate'] = texts[1]
                    item['educations'].append(education)

            elif '工作经历'.decode('utf-8') in block_title:
                for li in div.select('li'):
                    self.work_id += 1

                    work                    = WorkItem()
                    work['id']              = self.education_id
                    work['investor_id']     = item['id']
                    texts = [x.strip() for x in li.h6.get_text().split('&bullet;', 1)]
                    work['name'] = texts[0]
                    if len(texts) >= 2:
                        work['position'] = texts[1]

                    if li.p:
                        texts = [x.strip() for x in li.p.get_text().split('-', 1)]
                        work['startDate'] = texts[0]
                        if len(texts) >= 2:
                            work['endDate'] = texts[1]
                    item['works'].append(work)

        item['qas'] = []
        for li in soup.select('.block-qa .qa-list li'):
            self.qa_id += 1

            qa                  = QAItem()
            qa['id']            = self.qa_id
            qa['investor_id']   = item['id']
            qa['question']      = li.h6.get_text().split('：'.decode('utf-8'), 1)[1]
            qa['answer']        = li.select_one('.answer-content').get_text()
            item['qas'].append(qa)

        yield item

