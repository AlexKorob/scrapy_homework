# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class WarehouseItem(Item):
    category = Field()
    company = Field()
    title = Field()
    images = Field()
    sizes = Field()
    price = Field()
    description = Field()
    url = Field()
