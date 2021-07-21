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
    def __init__(self):
        dotenv_path = Path('../../.env')
        load_dotenv(dotenv_path=dotenv_path)

        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

        try:
            self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE=' +
                                       self.database+';User='+self.username+';Password='+self.password)
        except pyodbc.Error as err:
            logging.error(err)

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item["productNumber"] == None:
            logging.warning("Product Number is None")
            return item

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
        except pyodbc.Error as err:
            logging.error(err)

        self.conn.commit()
        logging.debug("Item stored: {}".format(item["productName"]))
