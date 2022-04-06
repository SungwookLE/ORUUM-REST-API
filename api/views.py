# oruum-rest-api/api/views.py

from cgitb import lookup
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import StockPriceSerializers, StockInformationSerializers, StockHistorySerializers
from api.models import StockPrice, StockInformation, StockHistory


class StockPageNumberPagination(PageNumberPagination):
    page_size=10


class StockPrice_ListCreateAPIView(ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializers
    pagination_class = StockPageNumberPagination


class StockPrice_RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = StockPrice.objects.all()
    lookup_field="symbol"
    serializer_class = StockPriceSerializers


class StockInformation_ListCreateAPIView(ListCreateAPIView):
    queryset = StockInformation.objects.all()
    serializer_class = StockInformationSerializers
    pagination_class = StockPageNumberPagination


class StockInformation_RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = StockInformation.objects.all()
    lookup_field = "symbol"
    serializer_class = StockInformationSerializers

class StockHistory_ViewSet(ModelViewSet):
    serializer_class = StockHistorySerializers 
    pagination_class = StockPageNumberPagination 
    lookup_field = "date"

    def get_queryset(self):
        return StockHistory.objects.filter(symbol=self.kwargs["symbol"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)