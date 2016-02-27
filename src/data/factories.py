# --*-- coding: utf-8 -*-

# import factory
import factory

# import data models
from data.models import Exchange, DataVendor, Symbol, DailyPrice


class ExchangeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Exchange

    abbrev = factory.Sequence(lambda n: "DSE-{0}".format(n))
    name   = factory.Sequence(lambda n: 'Stock Exchange-{0}'.format(n))
    city   = 'Toronto'
    country = 'Canada'
    currency = 'CAD'

class DataVendorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DataVendor

    name = factory.Sequence(lambda n: 'Vendor-{0}'.format(n))
    historical_url = factory.Sequence(lambda n: 'www.history{0}.com'.format(n))
    quotes_url = factory.Sequence(lambda n: 'www.quotes{0}.com'.format(n))
    support_email = factory.Sequence(lambda n: 'support@vendor.com'.format(n))


class SymbolFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Symbol

    exchange = factory.SubFactory(ExchangeFactory)
    ticker = factory.Sequence(lambda n: 'ABC-{0}'.format(n))
    name = factory.LazyAttribute(lambda n: '{.ticker} Company'.format(n))
    sector = 'Industrials'
    instrument = 'Equity'
    currency = 'CAD'

class DailyPriceFactory(factory.django.DjangoModelFactory):

    class Meta:
         model = DailyPrice

    data_vendor = factory.SubFactory(DataVendorFactory)
    symbol = factory.SubFactory(SymbolFactory)
    price_date = '1986-04-20'
    open_price = 1.40
    high_price = 1.60
    low_price  = 1.32
    close_price = 1.54
    adj_close_price = 1.54
    volume = 100000
