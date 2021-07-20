import scrapy
from scrapy.exceptions import CloseSpider
import logging
from items import ProductItem 

#Crawler for JAR Computers
class JarcomputersSpider(scrapy.Spider):
    #Name of the spider
    name = 'jarcomputers'
    allowed_domains = ['jarcomputers.com']
    #Where to start crawling
    start_urls = ['https://www.jarcomputers.com/search?q=']
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
            "productName": response.xpath("""/html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/h1/text()""")
                                .get()
                                .split(',')[0],
            "productNumber": response.xpath("""/html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li[4]/b/text()""").get(),
            "productStore": "jarcomputers",	
        }   

        isProductAvailable =response.xpath("""/html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li[6]/span/text()""").get()
        
        #Check if the product is not avaible
        if isProductAvailable == "Няма наличност" or isProductAvailable == "Стар продукт" or isProductAvailable == "Не е наличен":
            item['isProductAvailable'] = False
            item['productPrice'] = None
        else:
            item["isProductAvailable"] = True
            item['productPrice'] = float(response.xpath("""//*[@class="price"]/text()""").get() + response.xpath("""//*[@class="price2"]/text()""").get())

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
        #logging.getLogger('scrapy').propagate = False

        #Find all the hrefs
        self.href = response.xpath("""/html/body/div[3]/div[3]/div[2]/div/div[4]/ol/li/div[2]/p/span[2]/a/@href""").extract()

        #If there aren't any products, stop the crawl
        if self.href == []:
            raise CloseSpider('No products found')

        #Send requests to the hrefs and callback the method extractInfo
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
        
