from django.urls import path, include, register_converter
from rest_framework import routers
from api.converters import DateConverter

from api.views import Stock_List_ListCreateAPIView, Stock_List_RetrieveUpdateAPIView, Stock_Information_History_ListCreateAPIView, Stock_Information_History_RetrieveUpdateAPIView, Stock_Price_History_ViewSet
from api.views import User_List_ListCreateAPIView, User_List_RetrieveUpdateAPIView, User_Interest_ListCreateAPIView, User_Portfolio_ListCreateAPIView

app_name = 'api'
register_converter(DateConverter, 'date')

urlpatterns = [
    path('stocklist/', Stock_List_ListCreateAPIView.as_view(), name='stock_list-list'),
    path('stocklist/<str:ticker>/', Stock_List_RetrieveUpdateAPIView.as_view(), name='stock_list-detail'),

    path('stockinformationhistory/', Stock_Information_History_ListCreateAPIView.as_view(), name='stock_information_history-list'),
    path('stockinformationhistory/<str:ticker>/', Stock_Information_History_RetrieveUpdateAPIView.as_view(), name='stock_information_history-detail'),

    path('stockpricehistory/<str:ticker>/', Stock_Price_History_ViewSet.as_view(actions={
        'get':'list'
    }), name='stock_price_history-list'),
    
    path('stockpricehistory/<str:ticker>/<date:update_day>', Stock_Price_History_ViewSet.as_view(actions={
            'get':'retrieve'
        }
    ), name='stock_price_history-detail'),


    path('userlist/', User_List_ListCreateAPIView.as_view(), name='user_list-list'),
    path('userlist/<int:id_user>/', User_List_RetrieveUpdateAPIView.as_view(), name='user_list-detail'),

    path('userinterest/', User_Interest_ListCreateAPIView.as_view(), name='user_interest-list'),
    path('userportfolio/', User_Portfolio_ListCreateAPIView.as_view(), name='user_portfolio-list'),


]

