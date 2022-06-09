#  file: api/admin.py
from django.contrib import admin

from api.models import StockList, StockInformationHistory, StockPriceHistory


@admin.register(StockList)
class StockListAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'price', 'update_dt']
    search_fields = ['ticker']


@admin.register(StockInformationHistory)
class StockInformationHistoryAdmin(admin.ModelAdmin):
    search_fields = ['ticker']


@admin.register(StockPriceHistory)
class StockPriceHistoryAdmin(admin.ModelAdmin):
    search_fields = ['ticker']
    date_hierarchy = 'update_date'
