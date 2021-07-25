import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.ardes import ArdesSpider
from spiders.jarcomputers import JarcomputersSpider
from spiders.ardes import ArdesSpider
from spiders.emag import EmagSpider

def startCrawling(productToSearch):
    # Load the setting for scrapy
    process = CrawlerProcess(get_project_settings())

    # Set up logging
    logger = logging.getLogger('root')


    logger.info(
        "Starting crawler for " + productToSearch,
        extra={"tags": {"service": "crawler"}},
    )

    ArdesSpider.start_urls[0] += productToSearch
    JarcomputersSpider.start_urls[0] += productToSearch
    EmagSpider.start_urls[0] += productToSearch

    process.crawl(ArdesSpider)
    process.crawl(JarcomputersSpider)
    process.crawl(EmagSpider)
    process.start()