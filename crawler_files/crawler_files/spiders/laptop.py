import scrapy
import logging
from crawler_files.items import ProductItem 

class LaptopSpider(scrapy.Spider):
    productToSearch = input()
    name = 'laptop'
    allowed_domains = ['laptop.bg']
    start_urls = ['https://laptop.bg/search?q=' + productToSearch]
    href = []
    i = 0

    def extractInfo(self, response):
        item = ProductItem()
        item = {
                "productName": response.xpath("""/html/body/div[1]/article/form[2]/div/header/h1/text()""").get().replace("\n","").replace('"',""),
                "productStore": "Laptop.bg",
                "isProductAvailable": True,
                "productPrice": response.xpath("""/html/body/div[1]/article/form[2]/div/section/div[1]/div[1]/div[1]/span[2]/span[1]/text()""").get()
        }
        
        yield item
        self.i = self.i + 1
        if (self.i == self.href.__len__()):
            return
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)

    def parse(self, response):
        logging.getLogger('scrapy').propagate = False

        self.href = response.xpath("""//*[@class="products"]/li/article/a/@href""").extract()
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
