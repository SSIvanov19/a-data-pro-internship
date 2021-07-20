import scrapy
from scrapy.exceptions import CloseSpider
import logging
from items import ProductItem 

#Class: LaptopSpider
class EmagSpider(scrapy.Spider):
    #Name of the spider
    name = 'emag'
    allowed_domains = ['emag.bg']
    #Where to start crawling
    start_urls = ['https://www.emag.bg/search/']
    #List of href
    href = []
    i = 0

    #Method to extract data about a product
    #from the website catalogue
    def extractInfo(self, response):
        #Store the data in a ProductItem class
        item = ProductItem()

        #Store the data of the product
        item = {
                "productName": response.xpath("""//*[@id="page-skin"]/div[2]/div/div[1]/h1/text()""")
                                .get()
                                .split(',')[0]
                                .replace('\n', '')
                                .strip(),
                "productNumber": response.xpath("""//*[@id="page-skin"]/div[2]/div/div[1]/div[2]/span/text()""")
                                .get()
                                .split(' ')[3], 
                "productStore": "emag.bg",
                "imgForProductLink": response.xpath("""//*[contains(@class, 'product-gallery-image')]/@href""").get(),
                "isProductAvailable": True,
                "productPrice": float(response.xpath("""//p[contains(@class, 'product-new-price')]/text()""")
                                .get()
                                .replace('.', '')
                                .strip() + "." + 
                                response.xpath("""//p[contains(@class, 'product-new-price')]/sup/text()""")
                                .get())
        }

        #Send the data to the pipeline
        yield item

        #If there are not more product, stop the crawl
        self.i = self.i + 1
        if (self.i == self.href.__len__()):
            raise CloseSpider('Reached end of products')
        
        #Crawl the next product
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)

    #Method which finds the hrefs for the products
    def parse(self, response):
        #Stop the scrapy from sending logs
        logging.getLogger('scrapy').propagate = False

        #Store hrefs in a list
        self.href = response.xpath("""//*[@id="card_grid"]/div/div[2]/div/div[1]/a/@href""").extract()

        #If there aren't any products, stop the crawl
        if self.href == []:
            raise CloseSpider('No products found')

        #Send requests to the hrefs and callback the method extractInfo
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
