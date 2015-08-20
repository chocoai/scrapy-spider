# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spider_36kr.items import InvestorItem
from scrapy.exporters import CsvItemExporter

export_field = [
    'id',
    'kr_id',
    'name',
    'intro',
    'weibo',
    'weixin',
    'linkedin',
    'focusIntustry',
    'investCount',
    'investPhases',
    'investorSettings',
    'country',
    'city',
    'school',
]

investor_filename           = 'investor'
investor_company_filename   = 'investor_company'
investor_work_filename      = 'investor_work'
investor_investment_filename= 'investor_investment'

class InvestorPipeline(object):


    def __init__(self):
        self.exporters = {}

    def open_spider(self, spider):
        self.add_exporter(investor_filename)
        self.add_exporter(investor_company_filename)
        self.add_exporter(investor_work_filename)
        self.add_exporter(investor_investment_filename)

        for key, value in self.exporters.items():
            value['exporter'].start_exporting()

    def close_spider(self, spider):
        for key, value in self.exporters.items():
            value['exporter'].finish_exporting()
            value['file'].close()

    def process_item(self, item, spider):
        self.exporters[investor_filename]['exporter'].export_item(item)

        for company in item['companys']:
            self.exporters[investor_company_filename]['exporter'].export_item(company)

        for work in item['works']:
            self.exporters[investor_work_filename]['exporter'].export_item(work)

        for investment in item['investments']:
            self.exporters[investor_investment_filename]['exporter'].export_item(investment)

        return item

    def add_exporter(self, filename):
        file = open(filename + '.csv', 'w+b')
        self.exporters[filename] = {}
        self.exporters[filename]['file'] = file
        self.exporters[filename]['exporter'] = CsvItemExporter(
            file,
            fields_to_export = (export_field if filename == investor_filename else None)
        )
