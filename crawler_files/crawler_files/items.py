# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    productName = scrapy.Field()
    productNumber = scrapy.Field()
    productStore = scrapy.Field()
    isProductAvailable = scrapy.Field()
    productPrice = scrapy.Field()