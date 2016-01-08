# -*- coding: utf-8 -*-

import os

from datetime import datetime
from pytz import timezone

from lxml.html import parse
from urllib2 import urlopen
from math import ceil


# configure django
os.environ['DJANGO_SETTINGS_MODULE'] = 'db.settings'
import django
django.setup()

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


def create_exchanges(exchanges):

    """
    Save symbols to Symbol database mode.

    """

    # instantiate symbol objects
    exchange_objs = []
    for exchange in exchanges:
        exch = Exchange.objects.get_or_create(**exchange)


if __name__ == "__main__":
    exchanges = [
        { "abbrev": "NASDAQ",
          "name": "NASDAQ",
          "city": "New York",
          "country": "United States",
          "currency": "USD",
          "utc_offset":get_timezone_offset(),
      },
        { "abbrev": "NYSE",
          "name": "New York Stock Exchange",
          "city": "New York",
          "country": "United States",
          "currency": "USD",
          "utc_offset":get_timezone_offset(),
      },
        { "abbrev": "TSX",
          "name": "Toronto Stock Exchange",
          "city": "Toronto",
          "country": "Canada",
          "currency": "CAD",
          "utc_offset":get_timezone_offset(),
      }
    ]
    create_exchanges(exchanges)
