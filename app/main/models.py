# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Linkforeachproductinstore(models.Model):
    productid = models.OneToOneField('Products', models.DO_NOTHING, db_column='ProductId', primary_key=True)  # Field name made lowercase.
    storeid = models.ForeignKey('Stores', models.DO_NOTHING, db_column='StoreId')  # Field name made lowercase.
    link = models.CharField(db_column='Link', unique=True, max_length=400)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LinkForEachProductInStore'
        unique_together = (('productid', 'storeid'),)


class Pricesforeachstore(models.Model):
    productid = models.OneToOneField('Products', models.DO_NOTHING, db_column='ProductId', primary_key=True)  # Field name made lowercase.
    storeid = models.ForeignKey('Stores', models.DO_NOTHING, db_column='StoreId')  # Field name made lowercase.
    isavailable = models.BooleanField(db_column='IsAvailable')  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PricesForEachStore'
        unique_together = (('productid', 'storeid'), ('productid', 'storeid'),)


class Products(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    productnumber = models.CharField(db_column='ProductNumber', max_length=52)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255)  # Field name made lowercase.
    imglink = models.CharField(db_column='ImgLink', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Products'


class Stores(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    storename = models.CharField(db_column='StoreName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stores'
