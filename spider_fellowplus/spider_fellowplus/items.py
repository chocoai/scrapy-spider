# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestorItem(scrapy.Item):
    id              = scrapy.Field()
    name            = scrapy.Field()
    position        = scrapy.Field()
    brief           = scrapy.Field()
    investStart     = scrapy.Field()
    investCount     = scrapy.Field()
    investNextPhase = scrapy.Field()
    investQuit      = scrapy.Field()
    investPhases    = scrapy.Field()
    investLimit     = scrapy.Field()
    investPlan      = scrapy.Field()
    focusIntustry   = scrapy.Field()
    city            = scrapy.Field()
    investments     = scrapy.Field()
    educations      = scrapy.Field()
    works           = scrapy.Field()
    qas             = scrapy.Field()


class InvestmentItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    name        = scrapy.Field()
    brief       = scrapy.Field()
    phase       = scrapy.Field()


class EducationItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    school      = scrapy.Field()
    major       = scrapy.Field()
    startDate   = scrapy.Field()
    endDate     = scrapy.Field()


class WorkItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    name        = scrapy.Field()
    position    = scrapy.Field()
    startDate   = scrapy.Field()
    endDate     = scrapy.Field()


class QAItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    question    = scrapy.Field()
    answer      = scrapy.Field()
