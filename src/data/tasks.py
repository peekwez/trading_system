# -*- coding: utf-8 -*-
from __future__ import absolute_import

# import celert shared_task
from celery import shared_task

# import app utils
from data.utils import update_symbols, update_history, update_quotes

@shared_task
def add_symbols():
    update_symbols.update_db()

@shared_task
def add_historical_data_all():
    update_history().update_db()

@shared_task
def add_historical_data_ticker(tickers):
    update_history().update_db(tickers)
