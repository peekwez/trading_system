# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from datetime import date

from data.misc import yahoo_date_fmt, csv_to_sectors

DATA_VENDOR = {
    'yahoo': {
        'name':'Yahoo Finance',
        'historical_url':'http://ichart.finance.yahoo.com/table.csv',
        'quotes_url':'http://download.finance.yahoo.com/d/quotes.csv',
        'support_email':'support@yahoo.com',
    },
}

INDICES = {
    'S&P/TSX': {
        'constituents_url': 'http://web.tmxmoney.com/constituents_data.php?index=^TSX&index_name=S%26P%2FTSX+Composite+Index',
        'exchange': 'TSX',
    },
    'S&P/TSXV': {
        'constituents_url': 'http://web.tmxmoney.com/constituents_data.php?index=^JX&index_name=S%26P%2FTSX+Venture+Composite+Index',
        'exchange': 'TSXV'
    },
}

EXCHANGES = {
    'TSX': {
        "abbrev": "TSX",
        "name": "Toronto Stock Exchange",
        "city": "Toronto",
        "country": "Canada",
        "currency": "CAD"
    },
    'TSXV': {
        "abbrev": "TSXV",
        "name": "TSX Venture Exchange",
        "city": "Calgary",
        "country": "Canada",
        "currency": "CAD"
    }
}

QUOTES_MAP =  (
    (0,'price_date'),
    (1,'open_price'),
    (2,'high_price'),
    (3,'low_price'),
    (4,'close_price'),
    (5,'volume'),
    (6,'adj_close_price'),
)


FILE_PATH = os.path.join(os.path.dirname(__file__))
SECTOR_FILES = (
    (0, FILE_PATH + '/assets/tsx.csv'),
    (0, FILE_PATH + '/assets/tsxv.csv'),
    (1, FILE_PATH + '/assets/sec.csv'),
)

SECTOR_URL = 'http://apps.tmx.com/en/pdf/mig/TSX_TSXV_Issuers.xls'

SECTORS = csv_to_sectors(SECTOR_FILES)
