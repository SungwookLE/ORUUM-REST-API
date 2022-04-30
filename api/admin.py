from csv import list_dialects
from django.contrib import admin

from api.models import Stock_List, Stock_Information_History, Stock_Price_History

@admin.register(Stock_List)
class StockListAdmin(admin.ModelAdmin):
    list_display = ['ticker','price','update_dt']
    search_fields = ['ticker']

@admin.register(Stock_Information_History)
class StockInformationHistoryAdmin(admin.ModelAdmin):
    search_fields = ['ticker']
    date_hierarchy = 'update_date'

@admin.register(Stock_Price_History)
class StockPriceHistoryAdmin(admin.ModelAdmin):
    search_fields = ['ticker']
    date_hierarchy = 'update_date'