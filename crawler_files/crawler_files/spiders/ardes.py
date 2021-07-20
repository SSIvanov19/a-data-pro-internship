import scrapy
from scrapy.exceptions import CloseSpider
import logging
from items import ProductItem

#Crawler for Ardes
class ArdesSpider(scrapy.Spider):
    #Name of the spider
    name = 'ardes'
    allowed_domains = ['ardes.bg']
    #Where to start crawling
    start_urls = ['https://ardes.bg/products?q=']
    #List of href
    href = []
    i = 0

    #Method which extract the data from the product page
    def extractInfo(self, response):
        #Store the data in a ProductItem class
        item = ProductItem()

        #Store the data of the product
        item = {
            "productName": response.xpath("""//*[@id="cont_1"]/div/div[1]/h1/text()""")
                                .get()
                                .split('-')[0]
                                .replace('\n', '')
                                .strip(),
            "productNumber": response.xpath("""//*[@id="technical_parameters"]/div[1]/div/span[2]/span/text()""").get(),
            "productStore": "ardes",
            "imgForProductLink": "https://ardes.bg" + response.xpath("""//*[@id="bigImage"]/@src""").get(),
            "isProductAvailable": True,
            "productPrice": float(response.xpath("""//*[@id="price-tag"]/text()""").get() + response.xpath("""//*[@id="buying-info"]/div[1]/span[2]/sup/text()""").get())
        }

        #Send the data to the pipeline
        yield item

        #If there are not more product, stop the crawl
        self.i = self.i + 1
        if (self.i == self.href.__len__()):
            return
        
        #Crawl the next product
        yield response.follow(self.href[self.i], callback=self.extractInfo)


    #Method which finds the hrefs for the products
    def parse(self, response):
        #Stop the scrapy from sending logs
        logging.getLogger('scrapy').propagate = False

        #Find all the hrefs
        self.href = response.xpath("""//*[@id="ajax_content"]/div[2]/div[2]/div/div/div/div[1]/a/@href""").extract()

        #If there aren't any products, stop the crawl
        if self.href == []:
            raise CloseSpider('No products found')

        #Send requests to the hrefs and callback the method extractInfo
        yield response.follow(self.href[self.i], callback=self.extractInfo)