# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_fellowplus.items import InvestorItem
from scrapy.exporters import CsvItemExporter
import os


export_field = [
    'id',
    'src_id',
    'src',
    'name',
    'position',
    'brief',
    'investStart',
    'investCount',
    'investNextPhase',
    'investQuit',
    'investPhases',
    'investLimit',
    'investPlan',
    'focusIntustry',
    'city',
]

investor_filename           = 'investor'
investor_education_filename = 'investor_education'
investor_work_filename      = 'investor_work'
investor_investment_filename= 'investor_investment'
investor_qa_filename        = 'investor_qa'

class InvestorPipeline(object):


    def __init__(self):
        self.exporters = {}

    def open_spider(self, spider):
        self.add_exporter(investor_filename)
        self.add_exporter(investor_education_filename)
        self.add_exporter(investor_work_filename)
        self.add_exporter(investor_investment_filename)
        self.add_exporter(investor_qa_filename)

        for key, value in self.exporters.items():
            value['exporter'].start_exporting()

    def close_spider(self, spider):
        for key, value in self.exporters.items():
            value['exporter'].finish_exporting()
            value['file'].close()

    def process_item(self, item, spider):
        self.exporters[investor_filename]['exporter'].export_item(item)

        for education in item['educations']:
            self.exporters[investor_education_filename]['exporter'].export_item(education)

        for work in item['works']:
            self.exporters[investor_work_filename]['exporter'].export_item(work)

        for investment in item['investments']:
            self.exporters[investor_investment_filename]['exporter'].export_item(investment)

        for qa in item['qas']:
            self.exporters[investor_qa_filename]['exporter'].export_item(qa)

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
