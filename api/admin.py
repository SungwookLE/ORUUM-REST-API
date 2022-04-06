from csv import list_dialects
from django.contrib import admin

from api.models import StockPrice, StockInformation
from api.models import StockHistory

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol','date', 'name', 'market',
                    'price', 'open', 'prevclose', 'high', 'low', 'volume','update_dt','create_dt']


@admin.register(StockInformation)
class StockInformationAdmin(admin.ModelAdmin):
    list_display = [ 'symbol','date' ,
                     'total_assets', 'curruent_assets' ,'inventory',
                     'quick_assets','non_current_assets','investments', 
                     'tagible_assets', 'liabilities', 'current_liabilities',
                     'non_current_liabilities', 'total_assets_ratio', 'quick_assets_ratio',
                     'liabilities_ratio', 'total_revenue','gross_profit','operating_income','net_income',
                     'total_revenue_ratio','operating_income_ratio','net_income_ratio','operating_cash_flow', 'update_dt','create_dt']


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = [ 'symbol', 'date', 
                     'opens','high','low', 
                     'close', 'adj_close', 'volume','splits', 'dividends' ,'update_dt','create_dt',
                   ]
    
