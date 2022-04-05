from django.urls import path, include
from rest_framework import routers

from api.views import StockPriceListAPIView, StockPriceRetrieveAPIView, StockInformationListAPIView, StockInformationRetrieveAPIView

app_name = 'api'

urlpatterns = [
    path('stockprice/', StockPriceListAPIView.as_view(), name='stockprice-list'),
    path('stockprice/<str:symbol>/', StockPriceRetrieveAPIView.as_view(), name='stockprice-detail'),

    path('stockinformation/', StockInformationListAPIView.as_view(), name='stockinformation-list'),
    path('stockinformation/<str:symbol>/', StockInformationRetrieveAPIView.as_view(), name='stockinformation-detail'),
]

