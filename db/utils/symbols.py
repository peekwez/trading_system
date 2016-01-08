# -*- coding: utf-8 -*-

import os
import datetime

from lxml.html import parse
from urllib2 import urlopen
from math import ceil


# configure django
os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'
import django
django.setup()

# import database models
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
            try:
                sd['exchange'] = Exchange.objects.get(abbrev="TSX")
            except DoesNotExist:
                raise("TSX exchange does not exist yet. Please create it")

        # Create a tuple (for the DB format) and append to the grand list
        symbols.append(sd)

    return symbols

def create_securities_symbols(symbols):

    """
    Save symbols to Symbol database mode.

    """

    # instantiate symbol objects
    symbol_objs = []
    for symbol in symbols:
        sd = Symbol.objects.get_or_create(**symbol)

def update_snp500_exchanges():

    # get all S&P Symbols
    symbols = Symbol.objects.filter(currency="USD")

if __name__ == "__main__":
    symbols  = get_parse_wiki_index_list(index="S&P500")
    symbols += get_parse_wiki_index_list(index="S&P/TSX")
    create_securities_symbols(symbols)
