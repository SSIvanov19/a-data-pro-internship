# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import sqlite3


class CrawlerFilesPipeline:
    def __init__(self):
        """
        Creating a local sqlite database and
        creating the schema if it doesn't exist already. 
        """
        
        self.connection = sqlite3.connect("./data.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Products
            (
                Id INTEGER PRIMARY KEY, 
                ProductName VARCHAR(255),
                UNIQUE (ProductName) ON CONFLICT IGNORE
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Stores
            (
                Id INTEGER PRIMARY KEY, 
                StoreName VARCHAR(255),
                UNIQUE (StoreName) ON CONFLICT IGNORE
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PricesForEachStore
            (
                ProductId INTEGER, 
                StoreId INTEGER,
                IsAvailable INTEGER ALLOW NULL,
                Price REAL,
                UNIQUE (ProductId, StoreId) ON CONFLICT IGNORE
            )
            """
        )

    def process_item(self, item, spider):
        """
        Minimal item processing and inserting it into the
        database using the `self.connection` initialized
        in the constructor.
        """

        # self.cursor.execute(
        #     """INSERT INTO Data (productName, productStore, isProductAvailable, productPrice) values (?, ?, ?, ?)""",
        #     (item["productName"], item["productStore"], item["isProductAvailable"], item["productPrice"]),
        # )

        self.cursor.execute(
            """INSERT INTO Products (ProductName) values (?)""",
            (item["productName"],),
        )

        self.cursor.execute(
            """INSERT INTO Stores (StoreName) values (?)""",
            (item["productStore"],),
        )

        self.cursor.execute(
            """INSERT INTO PricesForEachStore (ProductId, StoreId, IsAvailable, Price) 
                SELECT
                (SELECT Id FROM Products WHERE ProductName = "{}") as ProductId,
                (SELECT Id FROM Stores WHERE StoreName = "{}") as StoreId,
                {}, {}"""
                .format(item["productName"], item["productStore"], item["isProductAvailable"], item["productPrice"]),
            )
        
        self.connection.commit()
        logging.debug("Item stored {}".format(item["productName"]))
        return item
