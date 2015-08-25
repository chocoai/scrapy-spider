# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestorItem(scrapy.Item):
    id          = scrapy.Field()
    itjuzi_id   = scrapy.Field()
    name        = scrapy.Field()
    position    = scrapy.Field()
    weibo       = scrapy.Field()
    brief       = scrapy.Field()
    address     = scrapy.Field()
    company     = scrapy.Field()
    school      = scrapy.Field()
    intustry    = scrapy.Field()
    investments = scrapy.Field()


class InvestmentItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    itjuzi_id   = scrapy.Field()
    name        = scrapy.Field()
    investDate  = scrapy.Field()
    phase       = scrapy.Field()
    amount      = scrapy.Field()
    company_url = scrapy.Field()

