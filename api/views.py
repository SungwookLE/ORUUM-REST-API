# oruum-rest-api/api/views.py

from cgitb import lookup
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import StockPriceSerializers, StockInformationSerializers, StockHistory_TSLA_Serializers
from api.models import StockPrice, StockInformation, StockHistory_TSLA


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
    #queryset = StockHistory_TSLA.objects.all()
    serializer_class = StockHistory_TSLA_Serializers
    pagination_class = StockPageNumberPagination 
    lookup_field = "date"

    def get_queryset(self):
        return StockHistory_TSLA.objects.filter(symbol=self.kwargs["symbol"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)