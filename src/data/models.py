# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from decimal import Decimal
import datetime

# import django models
from django.db import models

# Create your models here.
class CommonInfo(models.Model):

    """ Common Info for all models """
    created_date = models.DateTimeField(
        auto_now_add=True,
        null=False
    )

    last_updated_date = models.DateTimeField(
        auto_now=True,
        null=False
    )

    class Meta:
        abstract = True

class Exchange(CommonInfo):

    """ Exchange model """

    abbrev = models.CharField(
        max_length=32,
        null=False
    )

    name = models.CharField(
        max_length=255,
        null=False
    )

    city = models.CharField(
        max_length=255,
        null=True
    )

    country = models.CharField(
        max_length=255,
        null=True
    )

    currency = models.CharField(
        max_length=64,
        null=False
    )

    class Meta:
        unique_together = ("name",)

    def __str__(self):
        return self.abbrev

class DataVendor(CommonInfo):

    """ Data vendor model """

    name = models.CharField(
        max_length=255,
        null=False
    )

    historical_url = models.URLField(
        max_length=255,
        null=True
    )

    quotes_url = models.URLField(
        max_length=255,
        null=True
    )

    support_email = models.EmailField(
        max_length=255,
        null=True
    )

    def __str__(self):
        return self.name

class Symbol(CommonInfo):

    """ Symbol model """

    exchange = models.ForeignKey(
        'data.Exchange',
        related_name="symbols",
        related_query_name="symbol",
        null=True
    )

    ticker = models.CharField(
        max_length=255,
        null=False
    )

    instrument = models.CharField(
        max_length=64,
        null=False
    )

    name = models.CharField(
        max_length=255,
        null=True
    )

    sector = models.CharField(
        max_length=255,
        null=True
    )

    currency = models.CharField(
        max_length=32,
        null=True
    )

    class Meta:
        ordering = ("name", "ticker",)
        unique_together = ("ticker",)

    def __str__(self):
        return self.ticker

    @property
    def yahoo_ticker(self):
        ticker = self.ticker.replace('.','-')
        if self.exchange.abbrev == 'TSX':
            return ticker + ".TO"
        elif self.exchange.abbrev == 'TSXV':
            return ticker + ".V"

class DailyPrice(CommonInfo):

    """ Daily price model """

    data_vendor = models.ForeignKey(
        'data.DataVendor',
        related_name="daily_prices",
        related_query_name="daily_price",
        null=False
    )

    symbol = models.ForeignKey(
        'data.Symbol',
        related_name="daily_prices",
        related_query_name="daily_price",
        null=False
    )

    price_date = models.DateField()

    open_price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    high_price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    low_price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    close_price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    adj_close_price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    volume = models.IntegerField()

    class Meta:
        ordering = ('-price_date','symbol')
        unique_together = ("symbol", "price_date")


class Portfolio(models.Model):

    """ Portfolio model """

    name = models.CharField(
        max_length=255,
    )

    reporting_name =  models.CharField(
        max_length=30,
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        null=False
    )

    symbols = models.ManyToManyField(
        "data.Symbol",
        through="data.Lot",
        related_name="portfolios",
        related_query_name="portfolio",
    )

    def __init__(self,*args,**kwargs):
        super(Portfolio,self).__init__(*args,**kwargs)
        self.__compute()

    def __str__(self):
        return self.reporting_name

    def __compute(self):
        self.__value = Decimal(0.)
        self.__cost  = Decimal(0.)
        self.__gain  = Decimal(0.)

        for lot in self.lots.all():
            prices = lot.symbol.daily_prices.all().filter(
                price_date__lte=datetime.date.today(),
            ).order_by("-price_date")[:2]
            new = Decimal(prices[0].close_price)
            old = Decimal(prices[1].close_price)
            print prices[0].price_date,new,prices[1].price_date,old

            self.__value += lot.quantity*new
            self.__gain  += lot.quantity*(new-old)
            self.__cost  += lot.quantity*lot.price+lot.fees
        self.__pl = self.__value-self.__cost

    @property
    def value(self):
        return round(self.__value,2)

    @property
    def cost(self):
        return round(self.__cost,2)

    @property
    def daily_gain(self):
        return round(self.__gain,2)

    @property
    def p_l(self):
        return round(self.__pl,2)

class Lot(models.Model):

    """ Lot model """

    portfolio = models.ForeignKey(
        "data.Portfolio",
        related_name="lots",
        related_query_name="lot",
    )

    symbol = models.ForeignKey(
        "data.Symbol",
        related_name="lots",
        related_query_name="lot",
    )

    date = models.DateField()

    quantity = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=19,
        decimal_places=4
    )

    fees = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )

    def __str__(self):
        return "{0:s}".format(self.symbol.ticker)
