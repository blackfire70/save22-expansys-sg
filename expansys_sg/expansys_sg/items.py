# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ExpansysItem(scrapy.Item):    
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    currency = scrapy.Field()
    price=scrapy.Field()
    sku = scrapy.Field()
    time = scrapy.Field()
    category = scrapy.Field()
    ean = scrapy.Field()
    primary_image_url = scrapy.Field()
    availability = scrapy.Field()
    brand = scrapy.Field()
    pass
