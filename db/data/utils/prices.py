# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from copy import deepcopy

from urllib2 import urlopen

import pandas as pd


# import database models
from data.utils.misc import bcolors
from data.models import Symbol, DataVendor, DailyPrice

def add_historical_prices():
    '''
    Adds 10 years of hostorical prices for all companies
    in database including today

    Data Vendor: Yahoo Finance

    '''

    # delete all historical data
    DailyPrice.objects.all().delete()

    # get today's date
    end_date   = date.today().timetuple()

    # get date params for query
    date_params = "a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"%(
        str(0).zfill(2), str(1).zfill(2), str(end_date[0]-10),
        str(end_date[1]-1).zfill(2), str(end_date[2]).zfill(2), str(end_date[0]),
    )

    # get vendor url
    data_vendor = DataVendor.objects.get(name="Yahoo Finance")
    base_url = data_vendor.historical_url

    # get all symbols
    symbols = Symbol.objects.all()
    for symbol in symbols:
        params = "?s=%s&" %symbol.ticker + date_params
        site_url = base_url + params
        try:
            response = urlopen(site_url)
            data = pd.read_csv(response)
            add_to_db(symbol,data_vendor,data)
        except Exception, e:
            print(bcolors.WARNING + "Could not add historical prices for %s: %s" %(symbol.ticker, e) + bcolors.ENDC)


def add_prices_for_tickers(tickers, start_date=None):
    '''
    Adds hostorical prices for companies specified
    starting from the specified date to today's date.

    Data Vendor: Yahoo Finance

    '''

    # delete data for tickers
    DailyPrice.objects.filter(symbol__ticker__in=tickers).delete()

    # get date for symbol
    end_date   = date.today().timetuple()
    if start_date == None:
        start_date = deepcopy(end_date)
    else:
        start_date = date(start_date).timetuple()

    # get date params for query
    date_params = "a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"%(
        str(start_date[1]-1).zfill(2), str(start_date[2]).zfill(2), str(end_date[0]-10),
        str(end_date[1]-1).zfill(2), str(end_date[2]).zfill(2), str(end_date[0]),
    )

    # get vendor url
    data_vendor = DataVendor.objects.get(name="Yahoo Finance")
    base_url = data_vendor.historical_url



    # get symbols and update them
    symbols = Symbol.objects.filter(ticker__in=tickers)
    for symbol in symbols:
        params = "?s=%s&" %symbol.ticker + date_params
        site_url = base_url + params
        try:
            response = urlopen(site_url)
            data = pd.read_csv(response)
            add_to_db(symbol,data_vendor,data)
        except Exception, e:
            print(bcolors.WARNING + "Could not add historical prices for %s: %s" %(symbol.ticker, e) + bcolors.ENDC)


def update_prices():
    '''
    Updates daily prices of all companies in the database

    Data Vendor: Yahoo Finance
    '''

    data_vendor = DataVendor.objects.get(name="Yahoo Finance")
    base_url    = data_vendor.quotes_url

    symbols = Symbol.objects.all()

    # join all tickers to query
    # {n=name,s=symbol,o=open_price,h=high_price,g=low_price,l1=lastest_value,v=volume }
    params = "?s=" + ",".join(sym.ticker for sym in symbols) + "&f=nsohgl1v"

    # get query url
    site_url = base_url + params
    today = date.today()
    try:
        response = urlopen(site_url)
        data = pd.read_csv(response, header=None)
        nr_data = len(data)
    except Exception, e:
        raise Exception(bcolors.FAIL + "Could not fetch quotes: %s" %e + bcolors.ENDC)


    # update prices
    for k in range(nr_data):
        ticker = data.loc[k,1]
        try:
            symbol = symbols.get(ticker=ticker)
            quote  = {'open_price': float(data.loc[k,2]),
                      'high_price':  float(data.loc[k,3]),
                      'low_price': float(data.loc[k,4]),
                      'close_price': float(data.loc[k,5]),
                      'adj_close_price': float(data.loc[k,5]),
                      'volume': int(data.loc[k,6]),
                      'data_vendor': data_vendor,
            }
            price, created = DailyPrice.objects.update_or_create(
                symbol=symbol, price_date=today, defaults = quote)
        except Exception, e:
            print(bcolors.WARNING + "Could not update quote for %s:  %s" %(ticker,e) + bcolors.ENDC)


def add_to_db(symbol,data_vendor,data):
    '''
    Utility function for adding an ordered daily
    prices
    '''

    key_map = {
        'price_date': 'Date',
        'open_price': 'Open',
        'high_price': 'High',
        'low_price': 'Low',
        'close_price': 'Close',
        'adj_close_price': 'Adj Close',
        'volume': 'Volume'
    }

    prices = []
    nr_data = len(data)
    for i in range(nr_data):
        price = {'symbol': symbol, 'data_vendor': data_vendor}
        for key in key_map:
            data_key = key_map[key]
            price[key] = data.loc[i,data_key]
        prices.append(DailyPrice(**price))

    # bulk create all data
    DailyPrice.objects.bulk_create(prices)
