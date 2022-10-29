# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    id          = scrapy.Field()
    title       = scrapy.Field()
    author      = scrapy.Field()
    date        = scrapy.Field()
    messages    = scrapy.Field()

class MessageItem(scrapy.Item):
    id          = scrapy.Field()
    author      = scrapy.Field()
    date        = scrapy.Field()
    content     = scrapy.Field()


