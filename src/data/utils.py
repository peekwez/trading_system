# -*- coding: utf-8 -*-
from __future__ import absolute_import

from urllib2 import urlopen
from datetime import date
import time

import csv

from data.misc import info
from data.models import DataVendor, Exchange, Symbol, DailyPrice
from data.constants import (DATA_VENDOR, INDICES, EXCHANGES,
                            QUOTES_MAP, YAHOO_DATE_FMT,
                            SECTOR_URL, SECTORS)



yahoo,created = DataVendor.objects.get_or_create(**DATA_VENDOR['yahoo'])
yahoo_history = lambda ticker: yahoo.historical_url + '?s={0:s}&'.format(ticker) + YAHOO_DATE_FMT
yahoo_quotes = lambda tickers: yahoo.quotes_url+'?s='+','.join(ticker for ticker in tickers) + '&f=nsohgl1v'

def yahoo2db_tickers(ticker):
    return ticker.split('.')[0].replace('-','.')

def sectors(ticker):
    try:
        return SECTORS[ticker]
    except KeyError:
        return None


class BaseUtility(object):

    def __init__(self, model):
        self.model = model

    def open_url(self, site_url):
        return urlopen(site_url)

    def update_db(self,*args,**kwargs):
        pass



class IndexSymbols(BaseUtility):

    def __fetch_symbols(self,index):
        site_url = index['constituents_url']
        try:
            response = self.open_url(site_url)
        except Exception,e:
            raise Exception(info.FAIL + "Could not open {0:s}: {1:s}".format(site_url,e) + info.ENDC)
        else:
            return csv.reader(response)

    def __valid_line(self,line):
        return len(line) == 2 and line[1].find('Symbol') == -1

    def update_db(self):

        for key in INDICES:
            index = INDICES[key]
            data  = self.__fetch_symbols(index)
            index_kwargs = EXCHANGES[index['exchange']]
            exchange = Exchange.objects.get_or_create(**index_kwargs)[0]
            for line in data:
                if self.__valid_line(line):
                    name = line[0]
                    ticker = line[1]
                    kwargs = {
                        'name': name,
                        'ticker': ticker,
                        'exchange': exchange,
                        'currency': 'CAD',
                        'instrument': 'Equity',
                        'sector': sectors(ticker),
                    }
                    self.model.objects.update_or_create(
                        ticker=ticker,
                        defaults=kwargs
                    )


class ManualSymbol(IndexSymbols):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        super(ManualSymbol, self).__init__(*args,**kwargs)


    def update_db(self):
        pass

class YahooHistory(BaseUtility):

    def __fetch_history(self,symbol):
        ticker = symbol.yahoo_ticker
        try:
            response = self.open_url(yahoo_history(ticker))
        except Exception, e:
            print(info.WARNING + "Could not fetch historical prices for {0:s}: {1:s}".format(ticker,e) + info.ENDC)
            return None
        else:
            return csv.reader(response)

    def __extra_kwargs(self,kwargs,line):
        extra_kwargs = {'{0:s}'.format(key):line[k] for k,key in QUOTES_MAP}
        kwargs.update(extra_kwargs)
        return kwargs

    def update_db(self,tickers=None):
        create_size = 100000
        if tickers == None:
            symbols = Symbol.objects.all()
        else:
            symbols = Symbol.objects.filter(ticker__in=tickers)
        self.model.objects.filter(symbol__in=symbols).delete()

        total_elapsed = 0.
        objs = []
        nr_syms = symbols.count()
        for k,symbol in enumerate(symbols):
            data = self.__fetch_history(symbol)
            if data is not None:
                next(data,None) # skip header
                kwargs = {
                    'symbol':symbol,
                    'data_vendor': yahoo,
                }
                objs.extend(self.model(**self.__extra_kwargs(kwargs,line)) for line in data)

            if len(objs) > create_size: self.model.objects.bulk_create(objs); objs = []
            if k == nr_syms -1: self.model.objects.bulk_create(objs); objs = []



class YahooQuotes(BaseUtility):

    def __fetch_quotes(self,tickers):
        try:
            response = self.open_url(yahoo_quotes(tickers))
        except Exception, e:
            raise Exception(info.FAIL + "Could not fetch quotes: %s" %e + info.ENDC)
        else:
            return csv.reader(response)

    def update_db(self):
        symbols = Symbol.objects.all()
        tickers = [symbol.yahoo_ticker for symbol in symbols]
        data = self.__fetch_quotes(tickers)
        today = date.today()
        for line in data:
            ticker = yahoo2db_tickers(line[1])
            symbol = symbols.get(ticker=ticker)
            try:
                quote = {
                    'open_price': float(line[2]),
                    'high_price': float(line[3]),
                    'low_price': float(line[4]),
                    'close_price': float(line[5]),
                    'adj_close_price': float(line[5]),
                    'volume': int(line[6]),
                    'data_vendor': yahoo
                }
            except ValueError:
                print("Update of %s ignored due to bad data" %(symbol))
            else:
                self.model.objects.update_or_create(
                    symbol=symbol,
                    price_date=today,
                    defaults=quote
                )

update_symbols = IndexSymbols(model=Symbol)
update_history = YahooHistory(model=DailyPrice)
update_quotes  = YahooQuotes(model=DailyPrice)
