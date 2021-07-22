# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pyodbc
import logging
import os
from dotenv import load_dotenv
from pathlib import Path


class CrawlerFilesPipeline:
    # Set up logging
    logger = logging.getLogger('root')

    def __init__(self):
        # Path to .env file
        dotenv_path = Path('../../.env')
        load_dotenv(dotenv_path=dotenv_path)

        # Load the data from .env file
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

        # Try to connect to database
        try:
            self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE=' +
                                       self.database+';User='+self.username+';Password='+self.password)
        except pyodbc.Error as err:
            self.logger.error(err,
                              extra={"tags": {"service": "MSSQL"}})

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # Check if the item has a product number
        if item["productNumber"] == None:
            self.logger.warning('Product Number on product with name: "{}" is None/Null'.format(item["productName"]),
                                extra={"tags": {"service": "crawler"}})
            return item

        # Try to insert the item into the database
        try:
            self.returnValue = self.cursor.execute(
                """EXEC AddProduct
                @ProductNumber = ?,
                @ProductName = ?,
                @ProductStore = ?,
                @ImgLink = ?,
                @UrlLink = ?,
                @IsProductAvailable = ?,
                @ProductPrice = ?""",
                (item["productNumber"],
                 item["productName"],
                 item["productStore"],
                 item["imgForProductLink"],
                 item["urlLink"],
                 item["isProductAvailable"],
                 item["productPrice"])
            )
            self.conn.commit()
        except pyodbc.Error as err:
            self.logger.error(err,
                              extra={"tags": {"service": "MSSQL"}})

        self.logger.info("Item stored: {}".format(item["productName"]),
                         extra={"tags": {"service": "MSSQL"}})
