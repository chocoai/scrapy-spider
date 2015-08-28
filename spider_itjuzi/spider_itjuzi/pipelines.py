# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spider_itjuzi.items import InvestorItem
from scrapy.exporters import CsvItemExporter
import os

export_field = [
    'id',
    'src_id',
    'src',
    'name',
    'position',
    'weibo',
    'brief',
    'address',
    'company',
    'school',
    'intustry',
]

investor_filename           = 'investor'
investor_investment_filename= 'investor_investment'
investor_work_filename      = 'investor_work'

class InvestorPipeline(object):


    def __init__(self):
        self.exporters = {}

    def open_spider(self, spider):
        self.add_exporter(investor_filename)
        self.add_exporter(investor_investment_filename)
        self.add_exporter(investor_work_filename)

        for key, value in self.exporters.items():
            value['exporter'].start_exporting()

    def close_spider(self, spider):
        for key, value in self.exporters.items():
            value['exporter'].finish_exporting()
            value['file'].close()

    def process_item(self, item, spider):
        self.exporters[investor_filename]['exporter'].export_item(item)

        for investment in item['investments']:
            self.exporters[investor_investment_filename]['exporter'].export_item(investment)

        for work in item['works']:
            self.exporters[investor_work_filename]['exporter'].export_item(work)

        return item

    def add_exporter(self, filename):
        if not os.path.exists('result/'):
            os.mkdir('result/')
        file = open('result/' + filename + '.csv', 'w+b')
        self.exporters[filename] = {}
        self.exporters[filename]['file'] = file
        self.exporters[filename]['exporter'] = CsvItemExporter(
            file,
            fields_to_export = (export_field if filename == investor_filename else None)
        )
