# --*-- coding: utf-8 -*-

import pytest

from data.factories import SymbolFactory

pytestmark = pytest.mark.django_db

class TestModels:

    def test_exchange(client, exchange):
        assert isinstance(exchange,object) == True
        assert exchange.country == 'Canada'
        assert exchange.currency == 'CAD'

    def test_data_vendor(client, data_vendor):
        assert isinstance(data_vendor,object) == True

    def test_symbol(client, symbol):
        assert isinstance(symbol,object) == True
        assert symbol.sector == 'Industrials'
        assert symbol.instrument == 'Equity'
        assert symbol.currency == 'CAD'

    def test_daily_price(client, daily_price):
        assert isinstance(daily_price,object) == True
        assert daily_price.price_date == '1986-04-20'
        assert daily_price.open_price == 1.40
        assert daily_price.high_price == 1.60
        assert daily_price.low_price == 1.32
        assert daily_price.close_price == 1.54
        assert daily_price.adj_close_price == 1.54
        assert daily_price.volume == 100000

    def test_yahoo_ticker_tsx(client, tsx):
        tsx_symbol = SymbolFactory(ticker='ABC.B', exchange=tsx)
        assert tsx_symbol.yahoo_ticker == 'ABC-B.TO'

    def test_yahoo_ticker_tsxv(client, tsxv):
        tsxv_symbol = SymbolFactory(ticker='ABC.B', exchange=tsxv)
        assert tsxv_symbol.yahoo_ticker == 'ABC-B.V'
