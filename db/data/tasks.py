# -*- coding: utf-8 -*-
from __future__ import absolute_import

# import celert shared_task
from celery import shared_task

# import app utils
from data.utils import symbols, prices

@shared_task
def update_prices():
    prices.update_prices()

@shared_task
def update_securities_symbols():
    symbols.update_securities_symbols()

@shared_task
def add_historical_prices():
    prices.add_historical_prices()
