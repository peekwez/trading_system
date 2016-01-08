#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from data.models import Exchange, DataVendor, Symbol, DailyPrice

# Register your models here.
@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "abbrev", "currency","city", "country",
                    "utc_offset", "created_date", "last_updated_date")
    list_filter = ("name", "country", "currency",)
    search_fields = ("name","abbrev")

@admin.register(DataVendor)
class DataVendorAdmin(admin.ModelAdmin):
    list_display = ("name", "website_url", "support_email","created_date",
                    "last_updated_date")
    list_filter = ("name",)
    search_fields = ("name",)

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "exchange", "currency",
                    "instrument", "sector", "created_date", "last_updated_date")
    list_filter = ("instrument", "sector", "currency",)
    search_fields = ("name", "ticker",)

@admin.register(DailyPrice)
class DailyPriceAdmin(admin.ModelAdmin):
    list_display = ("symbol", "price_date", "open_price",
                    "high_price", "low_price", "close_price",
                    "adj_close_price", "volume", "created_date",
                    "last_updated_date")
    list_filter = ("symbol",)
    search_fields = ("symbol",)
