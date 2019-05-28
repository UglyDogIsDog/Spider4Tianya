# -*- coding: utf-8 -*-

import scrapy


class SecondItem(scrapy.Item):
    passage = scrapy.Field()
    # view = scrapy.Field()


class FirstItem(scrapy.Item):
    title = scrapy.Field()
    passage = scrapy.Field()
    response = scrapy.Field()
