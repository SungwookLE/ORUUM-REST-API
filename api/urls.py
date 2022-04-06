from django.urls import path, include, register_converter
from rest_framework import routers
from api.converters import DateConverter

from api.views import StockPrice_ListCreateAPIView, StockPrice_RetrieveUpdateDestroyAPIView, StockInformation_ListCreateAPIView, StockInformation_RetrieveUpdateDestroyAPIView
from api.views import StockHistory_ViewSet

app_name = 'api'
register_converter(DateConverter, 'date')

urlpatterns = [
    path('stockprice/', StockPrice_ListCreateAPIView.as_view(), name='stockprice-list'),
    path('stockprice/<str:symbol>/', StockPrice_RetrieveUpdateDestroyAPIView.as_view(), name='stockprice-detail'),

    path('stockinformation/', StockInformation_ListCreateAPIView.as_view(), name='stockinformation-list'),
    path('stockinformation/<str:symbol>/', StockInformation_RetrieveUpdateDestroyAPIView.as_view(), name='stockinformation-detail'),

    # path('stockhistory/<str:symbol>/', StockHistory_ViewSet.as_view(actions={
    #     'get':'list'
    # }), name='stockhistory-list'),
    
    # path('stockhistory/<str:symbol>/<date:date>', StockHistory_ViewSet.as_view(
    #     actions={
    #         'get':'retrieve'
    #     }
    # ), name='stockhistory-detail'),

]

