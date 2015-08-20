# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class InvestorItem(scrapy.Item):
    id              = scrapy.Field()
    kr_id           = scrapy.Field()
    name            = scrapy.Field()
    intro           = scrapy.Field()
    weibo           = scrapy.Field()
    weixin          = scrapy.Field()
    linkedin        = scrapy.Field()
    focusIntustry   = scrapy.Field()
    investCount     = scrapy.Field()
    investPhases    = scrapy.Field()
    investorSettings= scrapy.Field()
    country         = scrapy.Field()
    city            = scrapy.Field()
    school          = scrapy.Field()
    companys        = scrapy.Field()
    works           = scrapy.Field()
    investments     = scrapy.Field()


class CompanyItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    kr_id       = scrapy.Field()
    brief       = scrapy.Field()
    startDate   = scrapy.Field()
    endDate     = scrapy.Field()
    kr_group_id = scrapy.Field()
    groupName   = scrapy.Field()
    isCurrent   = scrapy.Field()
    position    = scrapy.Field()


class WorkItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    kr_id       = scrapy.Field()
    brief       = scrapy.Field()
    startDate   = scrapy.Field()
    endDate     = scrapy.Field()
    kr_group_id = scrapy.Field()
    groupName   = scrapy.Field()
    isCurrent   = scrapy.Field()
    position    = scrapy.Field()


class InvestmentItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    kr_id       = scrapy.Field()
    kr_group_id = scrapy.Field()
    name        = scrapy.Field()
    brief       = scrapy.Field()
    industry    = scrapy.Field()
    investDate  = scrapy.Field()
    phase       = scrapy.Field()
    latestPhase = scrapy.Field()
    participant = scrapy.Field()
    amount      = scrapy.Field()
    amountUnit  = scrapy.Field()

