from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.ardes import ArdesSpider
from spiders.jarcomputers import JarcomputersSpider
from spiders.ardes import ArdesSpider
from spiders.emag import EmagSpider

productToSearch = input()

ArdesSpider.start_urls[0] += productToSearch
JarcomputersSpider.start_urls[0] += productToSearch
EmagSpider.start_urls[0] += productToSearch

process = CrawlerProcess(get_project_settings())
process.crawl(ArdesSpider)
process.crawl(JarcomputersSpider)
process.crawl(EmagSpider)
process.start()

exit()