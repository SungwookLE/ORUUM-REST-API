#  file: api/urls.py
from django.urls import path, register_converter
from api.converters import DateConverter

from api.views import StockListListAPIView, StockListRetrieveAPIView
from api.views import StockInformationHistoryListAPIView, StockInformationHistoryRetrieveAPIView, StockInformationSparkListAPIView
from api.views import StockPriceHistoryListAPIView, StockPriceHistoryRetrieveAPIView, StockPriceSparkListAPIView
from api.views import HistoricalStockPriceAPIView, StockSummaryAPIView, StockYearlyFinancialStatementsAPIView, StockQuarterlyFinancialStatementsAPIView, StockProfileAPIView


app_name = 'api'
register_converter(DateConverter, 'date')

urlpatterns = [
    path('stocklist/', StockListListAPIView.as_view(), name='stocklist-list'),
    path('stocklist/<str:ticker>/',
         StockListRetrieveAPIView.as_view(), name='stocklist-detail'),

    path('stockinformationhistory/<str:ticker>/',
         StockInformationHistoryListAPIView.as_view(), name='stockinformationhistory-list'),
    path('stockinformationhistory/<str:ticker>/<date:update_date>/',
         StockInformationHistoryRetrieveAPIView.as_view(), name='stockinformationhistory-detail'),
    path('stockinformationspark/<str:ticker>/<date:s_date>-<date:e_date>/',
         StockInformationSparkListAPIView.as_view(), name='stockinformationspark-list'),

    path('stockpricehistory/<str:ticker>/',
         StockPriceHistoryListAPIView.as_view(), name='stockpricehistory-list'),
    path('stockpricehistory/<str:ticker>/<date:update_date>/',
         StockPriceHistoryRetrieveAPIView.as_view(), name='stockpricehistory-detail'),
    path('stockpricespark/<str:ticker>/<date:s_date>-<date:e_date>/',
         StockPriceSparkListAPIView.as_view(), name='stockpricespark-list'),
    
    path('historicalstockprice/<str:ticker>/<date:s_date>-<date:e_date>/', 
          HistoricalStockPriceAPIView.as_view(), name='historicalstockprice-list'),
    path('stocksummary/<str:ticker>/', 
          StockSummaryAPIView.as_view(), name='stocksummary-detail'),
    path('stockyearlyfinancialstatements/<str:ticker>/',  
          StockYearlyFinancialStatementsAPIView.as_view(), name='stockyearlyfinancialstatements-detail'),
    path('stockquarterlyfinancialstatements/<str:ticker>/',  
          StockQuarterlyFinancialStatementsAPIView.as_view(), name='stockquarterlyfinancialstatements-detail'),
    path('stockprofile/<str:ticker>/',  
          StockProfileAPIView.as_view(), name='stockprofile-detail'), 
]
