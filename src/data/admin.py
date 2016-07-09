#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from data.models import Exchange, DataVendor, Symbol, DailyPrice, Portfolio, Lot

# Register your models here.
@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "abbrev", "currency","city", "country",
                    "created_date", "last_updated_date")
    list_filter = ("country", "currency",)
    search_fields = ("name","abbrev")

@admin.register(DataVendor)
class DataVendorAdmin(admin.ModelAdmin):
    list_display = ("name", "quotes_url", "historical_url", "support_email",
                    "created_date", "last_updated_date")
    search_fields = ("name",)

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "exchange", "currency",
                    "instrument", "sector", "created_date", "last_updated_date")
    list_filter = ("exchange", "instrument", "sector", "currency",)
    search_fields = ("name", "ticker", "exchange__abbrev")

@admin.register(DailyPrice)
class DailyPriceAdmin(admin.ModelAdmin):
    list_display = ("symbol", "price_date", "open_price",
                    "high_price", "low_price", "close_price",
                    "adj_close_price", "volume", "data_vendor",
                    "created_date", "last_updated_date")
    list_filter = ("price_date", "symbol__exchange", "symbol__currency")
    search_fields = ("symbol__ticker",)

class LotsInline(admin.TabularInline):
    model = Portfolio.symbols.through

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name", "reporting_name","created_date","colored_daily_gain","colored_pl","bold_value","bold_cost")
    inlines = (LotsInline,)
