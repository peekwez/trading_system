# --*-- coding: utf-8 -*-

import pytest

from data.factories import (ExchangeFactory,
                            DataVendorFactory,
                            SymbolFactory,
                            DailyPriceFactory
                            )

pytestmark = pytest.mark.django_dbase

@pytest.fixture(scope="class")
def exchange(dbase):
    return ExchangeFactory()

@pytest.fixture(scope="class")
def data_vendor(dbase):
    return DataVendorFactory()

@pytest.fixture(scope="class")
def symbol(dbase):
    return SymbolFactory()

@pytest.fixture(scope="class")
def daily_price(dbase):
    return DailyPriceFactory()

@pytest.fixture(scope="class")
def tsx(dbase):
    return ExchangeFactory(abbrev="TSX")

@pytest.fixture(scope="class")
def tsxv(dbase):
    return ExchangeFactory(abbrev="TSXV")
