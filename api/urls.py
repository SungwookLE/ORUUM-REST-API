from django.urls import path, include, register_converter
from rest_framework import routers
from api.converters import DateConverter

from api.views import Stock_List_CreateAPIView, Stock_List_RetrieveUpdateAPIView, Stock_Information_History_ListCreateAPIView, Stock_Information_History_RetrieveUpdateAPIView, Stock_Price_History_ViewSet

app_name = 'api'
register_converter(DateConverter, 'date')

urlpatterns = [
    path('stocklist/', Stock_List_CreateAPIView.as_view(), name='stock_list-list'),
    path('stocklist/<str:ticker>/', Stock_List_RetrieveUpdateAPIView.as_view(), name='stock_list-detail'),

    path('stockinformationhistory/', Stock_Information_History_ListCreateAPIView.as_view(), name='stock_information_history-list'),
    path('stockinformationhistory/<str:ticker>/', Stock_Information_History_RetrieveUpdateAPIView.as_view(), name='stock_information_history-detail'),

    path('stockpricehistory/<str:ticker>/', Stock_Price_History_ViewSet.as_view(actions={
        'get':'list'
    }), name='stock_price_history-list'),
    
    path('stockpricehistory/<str:ticker>/<date:date>', Stock_Price_History_ViewSet.as_view(actions={
            'get':'retrieve'
        }
    ), name='stock_price_history-detail'),

]

