from csv import list_dialects
from django.contrib import admin

from api.models import StockPrice, StockInformation

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'market','update_dt','create_dt',
                    'price', 'open', 'prevclose', 'high', 'low', 'volume' ]


@admin.register(StockInformation)
class StockInformationAdmin(admin.ModelAdmin):
    list_display = [ 'symbol', 'update_dt','create_dt',
                     'total_assets', 'curruent_assets' ,'inventory',
                     'quick_assets','non_current_assets','investments', 
                     'tagible_assets', 'liabilities', 'current_liabilities',
                     'non_current_liabilities', 'total_assets_ratio', 'quick_assets_ratio',
                     'liabilities_ratio', 'total_revenue','gross_profit','operating_income','net_income',
                     'total_revenue_ratio','operating_income_ratio','net_income_ratio','operating_cash_flow']

