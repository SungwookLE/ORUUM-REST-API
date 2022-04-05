# oruum-rest-api/api/views.py

from turtle import done
from django.shortcuts import render
from rest_framework import viewsets
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

from api.serializers import StockPriceSerializers, StockInformationSerializers
from api.models import StockPrice, StockInformation


class StockPageNumberPagination(PageNumberPagination):
    page_size=10


class StockPriceListAPIView(ListAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializers
    pagination_class = StockPageNumberPagination


class StockPriceRetrieveAPIView(RetrieveAPIView):
    queryset = StockPrice.objects.all()
    lookup_field="symbol"
    serializer_class = StockPriceSerializers
    

    
class StockInformationListAPIView(ListAPIView):
    queryset = StockInformation.objects.all()
    serializer_class = StockInformationSerializers
    pagination_class = StockPageNumberPagination


class StockInformationRetrieveAPIView(RetrieveAPIView):
    queryset = StockInformation.objects.all()
    lookup_field = "symbol"
    serializer_class = StockInformationSerializers
