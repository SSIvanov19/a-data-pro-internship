import os
import logging
import logging.handlers
import sentry_sdk
import logging_loki
from multiprocessing import Queue
from dotenv import load_dotenv
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler_files.crawler_files.spiders.ardes import ArdesSpider
from crawler_files.crawler_files.spiders.jarcomputers import JarcomputersSpider
from crawler_files.crawler_files.spiders.emag import EmagSpider


def startCrawling(productToSearch):
    # Load environment variables
    dotenv_path = Path("../.env")
    load_dotenv(dotenv_path=dotenv_path)

    # Set the minimal loggin level to Info
    logging.getLogger("requests").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    # Set up custom logger for scrapy
    # Set up logging handler
    handler = logging_loki.LokiQueueHandler(
        Queue(-1),
        url=os.getenv("LOKI_URL"),
        tags={"application": "a-data-pro-internship-test"},
        version="1",
    )

    # Add handler to the root logger
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    # Enable Sentry
    sentry_sdk.init(
        os.getenv("SENTRY_TOKEN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

    settings = get_project_settings()
    settings["ITEM_PIPELINES"] = {
        "crawler_files.crawler_files.pipelines.CrawlerFilesPipeline": 300,
    }

    # Set up crawler
    process = CrawlerProcess(settings)

    # Set up logging
    logger = logging.getLogger("root")

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
