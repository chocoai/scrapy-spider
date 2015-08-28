# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
import simplejson as json

city_map = []

def serializer_convert_timestamp(timestamp):
    if timestamp:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp/1000))
    else:
        return None

def serializer_convert_city(value):
    global city_map
    if len(city_map) == 0:
        f = open('data/city.json', 'r')
        city_map = json.load(f)
        f.close()
    items = filter(lambda a : a['id'] == value, city_map)
    if len(items) > 0:
        return items[0]['name'].encode('utf-8')
    else:
        return ''

def serializer_convert_invest_lmt_persion(value):
    ret = []
    if value.get('cnyInvestMin', ''):
        text = '￥%s万-￥%s万' \
            % (_get_invest_setting(value, 'cnyInvestMin'), \
               _get_invest_setting(value, 'cnyInvestMax'))
        ret.append(text)

    if value.get('usdInvestMin', ''):
        text = '$%s万-$%s万' \
            % (_get_invest_setting(value, 'usdInvestMin'), \
               _get_invest_setting(value, 'usdInvestMax'))
        ret.append(text)

    return ','.join(ret)

def serializer_convert_invest_lmt_org(value):
    ret = []
    if value.get('fundCnyInvestMin', ''):
        text = '￥%s万-￥%s万' \
            % (_get_invest_setting(value, 'fundCnyInvestMin'), \
               _get_invest_setting(value, 'fundCnyInvestMax'))
        ret.append(text)

    if value.get('fundUsdInvestMin', ''):
        text = '$%s万-$%s万' \
            % (_get_invest_setting(value, 'fundUsdInvestMin'), \
               _get_invest_setting(value, 'fundUsdInvestMax'))
        ret.append(text)

    return ','.join(ret)

def _get_invest_setting(setting, key):
    return filter(str.isdigit, setting.get(key, '').encode('utf-8'))

class InvestorItem(scrapy.Item):
    id                  = scrapy.Field()
    src_id              = scrapy.Field()
    src                 = scrapy.Field()
    name                = scrapy.Field()
    intro               = scrapy.Field()
    weibo               = scrapy.Field()
    weixin              = scrapy.Field()
    linkedin            = scrapy.Field()
    focusIntustry       = scrapy.Field()
    investCount         = scrapy.Field()
    investPhases        = scrapy.Field()
    investorSettings    = scrapy.Field()
    invest_lmt_person   = scrapy.Field(serializer=serializer_convert_invest_lmt_persion)
    invest_lmt_org      = scrapy.Field(serializer=serializer_convert_invest_lmt_org)
    country             = scrapy.Field(serializer=serializer_convert_city)
    city                = scrapy.Field(serializer=serializer_convert_city)
    school              = scrapy.Field()
    startups            = scrapy.Field()
    works               = scrapy.Field()
    investments         = scrapy.Field()


class StartupItem(scrapy.Item):
    id          = scrapy.Field()
    investor_id = scrapy.Field()
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

