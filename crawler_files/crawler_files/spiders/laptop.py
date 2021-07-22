import scrapy
from scrapy.exceptions import CloseSpider
import logging
from items import ProductItem 

#Class: LaptopSpider
class LaptopSpider(scrapy.Spider):
    #Name of the spider
    name = 'laptop'
    allowed_domains = ['laptop.bg']
    #Where to start crawling
    start_urls = ['https://laptop.bg/search?q=']
    #List of href
    href = []
    i = 0

    #Method to extract data about a product
    #from the website catalogue
    def extractInfo(self, response):
        self.logger.info('Extracting data from {}'.format(response.url),
                         extra={"tags": {"service": "crawler"}})

        #Store the data in a ProductItem class
        item = ProductItem()

        #Store the data of the product
        item = {
                "productName": response.xpath("""/html/body/div[1]/article/form[2]/div/header/h1/text()""").get().replace("\n","").replace('"',""),
                "productNumber": response.xpath("""//*[@id="product_id"]/@value""").extract()[0], 
                "productStore": "Laptop.bg",
                "isProductAvailable": True,
                "productPrice": float(response.xpath("""/html/body/div[1]/article/form[2]/div/section/div[1]/div[1]/div[1]/span[2]/span[1]/text()""").get())
        }
        
        #Send the data to the pipeline
        yield item

        #If there are not more product, stop the crawl
        self.i = self.i + 1
        if (self.i == self.href.__len__()):
            self.logger.info('No more products found',
                             extra={"tags": {"service": "crawler"}})
            raise CloseSpider('Reached end of products')
        
        #Crawl the next product
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)

    #Method which finds the hrefs for the products
    def parse(self, response):
        #Store hrefs in a list
        self.href = response.xpath("""//*[@class="products"]/li/article/a/@href""").extract()

        #If there aren't any products, stop the crawl
        if self.href == []:
            raise CloseSpider('No products found on: laptop.bg')

        #Send requests to the hrefs and callback the method extractInfo
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
