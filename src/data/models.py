# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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
