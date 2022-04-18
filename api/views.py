# oruum-rest-api/api/views.py

from cgitb import lookup
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import StockListSerializers, StockInformationHistorySerializers, StockPriceHistorySerializers
from api.models import Stock_List, Stock_Information_History, Stock_Price_History

from api.serializers import UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from api.models import User_List, User_Interest, User_Portfolio



class StockPageNumberPagination(PageNumberPagination):
    page_size=10


class Stock_List_ListCreateAPIView(ListCreateAPIView):
    queryset = Stock_List.objects.all()
    serializer_class = StockListSerializers
    pagination_class = StockPageNumberPagination


class Stock_List_RetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Stock_List.objects.all()
    lookup_field="ticker"
    serializer_class = StockListSerializers


class Stock_Information_History_ListCreateAPIView(ListCreateAPIView):
    queryset = Stock_Information_History.objects.all()
    serializer_class = StockInformationHistorySerializers
    pagination_class = StockPageNumberPagination


class Stock_Information_History_ViewSet(ModelViewSet):
    queryset = Stock_Information_History.objects.all()
    lookup_field = "date"
    serializer_class = StockInformationHistorySerializers

    def get_queryset(self):
        return Stock_Information_History.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class Stock_Price_History_ViewSet(ModelViewSet):
    serializer_class = StockPriceHistorySerializers 
    pagination_class = StockPageNumberPagination 
    lookup_field = "update_day"

    def get_queryset(self):
        return Stock_Price_History.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserPageNumberPagination(PageNumberPagination):
    page_size=10    


class User_List_ListCreateAPIView(ListCreateAPIView):
    queryset = User_List.objects.all()
    serializer_class = UserListSerializers
    pagination_class = UserPageNumberPagination


class User_List_RetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User_List.objects.all()
    lookup_field="id_user"
    serializer_class = UserListSerializers


class User_Interest_ListCreateAPIView(ListCreateAPIView):
    queryset = User_Interest.objects.all()
    serializer_class = UserInterestSerializers
    pagination_class = UserPageNumberPagination


class User_Portfolio_ListCreateAPIView(ListCreateAPIView):
    queryset = User_Portfolio.objects.all()
    serializer_class = UserPortfolioSerializers
    pagination_class = UserPageNumberPagination
    
