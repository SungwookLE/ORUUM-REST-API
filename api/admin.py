from csv import list_dialects
from django.contrib import admin

from api.models import StockPrice, StockInformation

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'market','update_dt','create_dt',
                    'price', 'open', 'prevclose', 'high', 'low', 'volume' ]


@admin.register(StockInformation)
class StockInformationAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'update_dt','create_dt',
                     'total_assets', 'curruent_assets' ,'inventory',
                     'quick_assets','non_current_assets','investments', 
                     'tagible_assets', 'liabilities', 'current_liabilities',
    ]