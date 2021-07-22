import logging
import logging_loki
import os
from dotenv import load_dotenv
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.ardes import ArdesSpider
from spiders.jarcomputers import JarcomputersSpider
from spiders.ardes import ArdesSpider
from spiders.emag import EmagSpider

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

# Set up logging handler
handler = logging_loki.LokiHandler(
    url=os.getenv('LOKI_URL'),
    tags={"application": "a-data-pro-internship-test"},
    version="1",
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('scrapy')
logger.addHandler(handler)
productToSearch = input()

logger.info(
    "Starting crawler for " + productToSearch,
    extra={"tags": {"service": "crawler"}},
)

ArdesSpider.start_urls[0] += productToSearch
JarcomputersSpider.start_urls[0] += productToSearch
EmagSpider.start_urls[0] += productToSearch

process = CrawlerProcess(get_project_settings())
process.crawl(ArdesSpider)
process.crawl(JarcomputersSpider)
process.crawl(EmagSpider)
process.start()

exit()
