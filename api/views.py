# oruum-rest-api/api/views.py

from cgitb import lookup
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import StockListSerializers, StockInformationHistorySerializers, StockPriceHistorySerializers
from api.models import Stock_List, Stock_Information_History, Stock_Price_History



class StockPageNumberPagination(PageNumberPagination):
    page_size=10


class Stock_List_CreateAPIView(ListCreateAPIView):
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


class Stock_Information_History_RetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Stock_Information_History.objects.all()
    lookup_field = "ticker"
    serializer_class = StockInformationHistorySerializers


class Stock_Price_History_ViewSet(ModelViewSet):
    serializer_class = StockPriceHistorySerializers 
    pagination_class = StockPageNumberPagination 
    lookup_field = "date"

    def get_queryset(self):
        return Stock_Price_History.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)