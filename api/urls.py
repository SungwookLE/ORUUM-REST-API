from django.urls import path, include
from rest_framework import routers

from api.views import StockPrice_ListCreateAPIView, StockPrice_RetrieveUpdateDestroyAPIView, StockInformation_ListCreateAPIView, StockInformation_RetrieveUpdateDestroyAPIView

app_name = 'api'

urlpatterns = [
    path('stockprice/', StockPrice_ListCreateAPIView.as_view(), name='stockprice-list'),
    path('stockprice/<str:symbol>/', StockPrice_RetrieveUpdateDestroyAPIView.as_view(), name='stockprice-detail'),

    path('stockinformation/', StockInformation_ListCreateAPIView.as_view(), name='stockinformation-list'),
    path('stockinformation/<str:symbol>/', StockInformation_RetrieveUpdateDestroyAPIView.as_view(), name='stockinformation-detail'),
]

