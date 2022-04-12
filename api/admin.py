from csv import list_dialects
from django.contrib import admin

from api.models import Stock_List, Stock_Information_History, Stock_Price_History
from api.models import User_List, User_Interest, User_Portfolio

@admin.register(Stock_List)
class StockListAdmin(admin.ModelAdmin):
    # list_display = ['symbol','date', 'name', 'market',
    #                 'price', 'open', 'prevclose', 'high', 'low', 'volume','update_dt','create_dt']
    pass

@admin.register(Stock_Information_History)
class StockInformationHistoryAdmin(admin.ModelAdmin):
    pass
   

@admin.register(Stock_Price_History)
class StockPriceHistoryAdmin(admin.ModelAdmin):
    pass
    
    
@admin.register(User_List)
class UserListAdmin(admin.ModelAdmin):
    pass
    
@admin.register(User_Interest)
class UserInterestAdmin(admin.ModelAdmin):
    pass
    
@admin.register(User_Portfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    pass