# -*- coding: utf-8 -*-
from __future__ import absolute_import

from lxml.html import parse
from urllib2 import urlopen

import pandas as pd

# import database models
from data.utils.misc import bcolors
from data.models import Symbol, Exchange


def get_parse_wiki_index_list(index="S&P500"):

    """
    Download and parse the Wikipedia list of S&P500
    or S&P/TSX constituents using requests and libxml.

    Returns a list of tuples for to add to the dabatase.

    """

    # Use libxml to download the list of S&P500 S&P/TSX companies and obtain the symbol table
    if index == "S&P500":
        site_url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    elif index == "S&P/TSX":
        site_url = 'http://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index'

    try:
        page = parse(site_url)
    except:
        page = parse(urlopen(site_url))

    # get correct slice of table
    if index == "S&P500":
        symbolslist = page.xpath('//table[1]/tr')[1:-2]
    elif index == "S&P/TSX":
        symbolslist = page.xpath('//table[1]/tr')[1:]


    # create symbols
    symbols = []
    for symbol in symbolslist:
        tds = symbol.getchildren()
        sd = {
            'ticker': tds[0].getchildren()[0].text,
            'name': tds[1].getchildren()[0].text,
            'instrument': "Equity",
        }

        if index == "S&P500":
            sd['sector'] = tds[3].text
            sd['currency'] = "USD"
        elif index == "S&P/TSX":
            sd['sector'] = tds[2].text
            sd['currency'] = "CAD"
            sd['ticker'] = sd['ticker'].replace('.','-') + ".TO" # Due to yahoo data
            try:
                sd['exchange'] = Exchange.objects.get(abbrev="TSX")
            except Exception, e:
                raise Exception(bcolors.FAIL + "TSX exchange does not exist yet. Please create it : %s" %e + bcolors.ENDC)

        # Create a tuple (for the DB format) and append to the grand list
        symbols.append(sd)

    return symbols

def update_snp500_exchanges():

    # get all S&P Symbols
    symbols = Symbol.objects.filter(currency="USD")
    exchanges = ('NASDAQ', 'NYSE')
    data = {}

    for exchange in exchanges:
        site_url = "http://www.nasdaq.com/screening/companies-by-name.aspx?exchange=%s&render=download" %(exchange)
        try:
            response = urlopen(site_url)
        except Exception, e:
            raise Exception(bcolors.FAIL + "Could not download company list for %s exchange : %s" %(exchange, e) + bcolors.ENDC)

        data[exchange] = pd.read_csv(response)['Symbol']

    for symbol in symbols:
        for key in data:
            if symbol.ticker in data[key].values:
                exchange = key
                break
        symbol.exchange = Exchange.objects.get(abbrev=exchange)
        symbol.save()

def update_securities_symbols():

    """
    Save symbols to Symbol database mode.

    """

    # get S&P symbols
    symbols  = get_parse_wiki_index_list(index="S&P500")
    symbols += get_parse_wiki_index_list(index="S&P/TSX")

    # instantiate symbol objects
    symbol_objs = []
    for symbol in symbols:
        sd = Symbol.objects.get_or_create(**symbol)


    # update exchanges for US symbols
    update_snp500_exchanges()
