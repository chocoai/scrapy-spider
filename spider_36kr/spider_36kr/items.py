# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
import simplejson as json

def serializer_convert_timestamp(timestamp):
    if timestamp:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp/1000))
    else:
        return None

def serializer_convert_city(value):
    global city_map
    city_map = []
    if len(city_map) == 0:
        f = open('data/city.json', 'r')
        city_map = json.load(f)
        f.close()
    items = filter(lambda a : a['id'] == value, city_map)
    print 'items:', len(items)
    if len(items) > 0:
        return items[0]['name'].encode('utf-8')
    else:
        return ''


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
    country         = scrapy.Field(serializer=serializer_convert_city)
    city            = scrapy.Field(serializer=serializer_convert_city)
    school          = scrapy.Field()
    startups        = scrapy.Field()
    works           = scrapy.Field()
    investments     = scrapy.Field()


class StartupItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    kr_id       = scrapy.Field()
    brief       = scrapy.Field()
    startDate   = scrapy.Field(serializer=serializer_convert_timestamp)
    endDate     = scrapy.Field(serializer=serializer_convert_timestamp)
    kr_group_id = scrapy.Field()
    groupName   = scrapy.Field()
    isCurrent   = scrapy.Field()
    position    = scrapy.Field()


class WorkItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
    kr_id       = scrapy.Field()
    brief       = scrapy.Field()
    startDate   = scrapy.Field(serializer=serializer_convert_timestamp)
    endDate     = scrapy.Field(serializer=serializer_convert_timestamp)
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
    investDate  = scrapy.Field(serializer=serializer_convert_timestamp)
    phase       = scrapy.Field()
    latestPhase = scrapy.Field()
    participant = scrapy.Field()
    amount      = scrapy.Field()
    amountUnit  = scrapy.Field()

