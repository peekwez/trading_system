# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone

# import database models
from data.models import Exchange


def  get_timezone_offset(tz="EST"):
    est = timezone(tz)
    dt = datetime.now()
    offset = est.utcoffset(dt).total_seconds()/3600
    value = ""
    if offset < 0:
        value = str(int(offset))
    elif offset > 0:
        value = "+" + str(int(offset))
    return "UTC{0:s}".format(value)


def create_exchanges():

    """
    Save symbols to Symbol database mode.

    """

    # hard code North American Exchanges
    exchanges = [
        { "abbrev": "NASDAQ",
          "name": "NASDAQ",
          "city": "New York",
          "country": "United States",
          "currency": "USD",
      },
        { "abbrev": "NYSE",
          "name": "New York Stock Exchange",
          "city": "New York",
          "country": "United States",
          "currency": "USD",
      },
        { "abbrev": "TSX",
          "name": "Toronto Stock Exchange",
          "city": "Toronto",
          "country": "Canada",
          "currency": "CAD",
      },
        {"abbrev": "TSXV",
         "name": "TSXV Venture Exchange",
         "city": "Toronto",
         "country": "Canada",
         "currency": "CAD",
     }
    ]

    # instantiate symbol objects
    exchange_objs = []
    for exchange in exchanges:
        exch = Exchange.objects.get_or_create(**exchange)
