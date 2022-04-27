from django.urls import path, include, register_converter
from rest_framework import routers
from api.converters import DateConverter

from api.views import Stock_List_ListAPIView, Stock_List_RetrieveAPIView
from api.views import Stock_Information_History_ListAPIView, Stock_Information_History_RetrieveAPIView, Stock_Information_Spark_ListAPIView 
from api.views import Stock_Price_History_ListAPIView, Stock_Price_History_RetrieveAPIView, Stock_Price_Spark_ListAPIView 
from api.views import User_List_ListAPIView, User_List_RetrieveAPIView, User_Interest_ListAPIView, User_Portfolio_ListAPIView

#from api.views import my_test_url, my_test2_url, my_test3_url, my_test_spark

app_name = 'api'
register_converter(DateConverter, 'date')

urlpatterns = [
    path('stocklist/', Stock_List_ListAPIView.as_view(), name='stock_list-list'),
    path('stocklist/<str:ticker>/', Stock_List_RetrieveAPIView.as_view(), name='stock_list-detail'),

    path('stockinformation_history/<str:ticker>/', Stock_Information_History_ListAPIView.as_view(), name='stock_information_history-list'),
    path('stockinformation_history/<str:ticker>/<date:update_date>/', Stock_Information_History_RetrieveAPIView.as_view(), name='stock_information_history-detail'),
    path('stockinformation_spark/<str:ticker>/<date:s_date>-<date:e_date>/', Stock_Information_Spark_ListAPIView.as_view(), name='stock_information_spark-list'),
    
    path('stockprice_history/<str:ticker>/', Stock_Price_History_ListAPIView.as_view(), name='stock_price_history-list'),
    path('stockprice_history/<str:ticker>/<date:update_date>/', Stock_Price_History_RetrieveAPIView.as_view(), name='stock_price_history-detail'),
    path('stockprice_spark/<str:ticker>/<date:s_date>-<date:e_date>/', Stock_Price_Spark_ListAPIView.as_view(), name='stock_price_spark-list'),
    
    path('userlist/', User_List_ListAPIView.as_view(), name='user_list-list'),
    path('userlist/<int:id_user>/', User_List_RetrieveAPIView.as_view(), name='user_list-detail'),

    path('userinterest/', User_Interest_ListAPIView.as_view(), name='user_interest-list'),
    path('userportfolio/', User_Portfolio_ListAPIView.as_view(), name='user_portfolio-list'),

]
### TEST: urls.py
"""
    path('my_test_url/<str:ticker>/', my_test_url, name='my_test'),
    path('my_test_spark/<str:ticker>/<date:s_date>-<date:e_date>/', my_test_spark, name='my_test'),

    path('my_test2_url/<str:ticker>/<date:s_date>-<date:e_date>/', my_test2_url.as_view(), name='my_test2'),
    path('my_test3_url/<str:ticker>/', my_test3_url.as_view(), name='my_test3_list'),
"""

