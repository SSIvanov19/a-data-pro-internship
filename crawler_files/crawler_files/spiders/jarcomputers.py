import scrapy
import logging
from crawler_files.items import ProductItem 

#Crawler for JAR Computers crawler
class JarcomputersSpider(scrapy.Spider):
    #What products to crawl
    productToSearch = input()
    #Name of the spider
    name = 'jarcomputers'
    allowed_domains = ['jarcomputers.com']
    #Where to start crawling
    start_urls = ['https://www.jarcomputers.com/search?q=' + productToSearch]
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
            "productNumber": response.xpath("""/html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li[5]/b/text()""").get(),
            "productStore": "jarcomputers",	
        }   

        #Check if the product is avaible
        if response.xpath("""/html/body/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/ul[1]/li[6]/span/text()""").get() != "Няма наличност":
            item["isProductAvailable"] = True
            item['productPrice'] = float(response.xpath("""//*[@id="price_label_id"]/text()""").get())
        else:
            item['isProductAvailable'] = False
            item['productPrice'] = None

        #Send the data to the pipeline
        yield item

        #If there are not more product, stop the crawl
        self.i = self.i + 1
        if (self.i == self.href.__len__()):
            return
        
        #Crawl the next product
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
        

    def parse(self, response):
        #Stop the scrapy from sending logs
        logging.getLogger('scrapy').propagate = False

        #Find all the hrefs
        self.href = response.xpath("""/html/body/div[3]/div[3]/div[2]/div/div[4]/ol/li/div[2]/p/span[2]/a/@href""").extract()
        #Send requests to the hrefs and callback the method extractInfo
        yield scrapy.Request(self.href[self.i], callback=self.extractInfo)
        
