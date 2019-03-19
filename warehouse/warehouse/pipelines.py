# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from my_site.tasks import save_warehouse_item


class WarehousePipeline:
    def __init__(self):
        self.limit_to_save = 10
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        if len(self.items) == self.limit_to_save or spider.worked:
            save_warehouse_item.delay(self.items)
            self.items = []
