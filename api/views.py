#  file: api/views.py

from calendar import week
import json

from cgitb import lookup
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


from api.serializers import StockListSerializer, StockInformationHistorySerializer, StockPriceHistorySerializer, HistoricalStockPriceSerializer
from api.models import StockList, StockInformationHistory, StockPriceHistory

import re
import datetime
from django.db.models import Max, Min, Avg

class StockPageNumberPagination(PageNumberPagination):
    page_size = 10


class StockListListAPIView(ListAPIView):
    queryset = StockList.objects.all()
    serializer_class = StockListSerializer
    pagination_class = StockPageNumberPagination


class StockListRetrieveAPIView(RetrieveAPIView):
    queryset = StockList.objects.all()
    lookup_field = "ticker"
    serializer_class = StockListSerializer


class StockInformationHistoryListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])


class StockInformationSparkListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])


class StockInformationHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class StockPriceHistoryListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])


class StockPriceSparkListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])


class StockPriceHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class HistoricalStockPriceAPIView(ListAPIView):
    serializer_class = HistoricalStockPriceSerializer

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])\
           .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]]).reverse()


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return_dict = dict()
        return_dict["ticker"] = self.kwargs["ticker"]
        return_dict["dateArray"] = list()
        return_dict["closeArray"] = list()
        return_dict["openArray"] = list()
        return_dict["highArray"] = list()
        return_dict["lowArray"] = list()
        return_dict["volumeArray"] = list()

        for idx, item in enumerate(serializer.data):
            iter_dict = json.loads(json.dumps(item))
            return_dict["dateArray"].append(iter_dict["update_date"])
            return_dict["closeArray"].append(iter_dict["price_close"])
            return_dict["openArray"].append(iter_dict["price_open"])
            return_dict["highArray"].append(iter_dict["price_high"])
            return_dict["lowArray"].append(iter_dict["price_low"])
            return_dict["volumeArray"].append(iter_dict["volume"])


        return Response(return_dict)


class StockSummaryAPIView(RetrieveAPIView):
    queryset = StockList.objects.prefetch_related()
    lookup_field="ticker"

    def get(self, request, ticker):
        obj = self.get_object()

        priceUnit = "dollar" if re.search("^NYSE|^Nasdaq", obj.market) else None

        endweek = datetime.datetime.today()
        startweek = endweek - datetime.timedelta(weeks=52)
        weekHigh52 = obj.stockpricehistory.filter(ticker=ticker, update_date__range=[startweek, endweek]).aggregate(price=Max('price_high'))
        weekLow52 = obj.stockpricehistory.filter(ticker=ticker, update_date__range=[startweek, endweek]).aggregate(price=Min('price_low'))

        # (9/28) PER, PBR 등 관련 정보 구현 아직입니다. (성욱)
        return Response({
            'ticker': obj.ticker,
            'koreanName': obj.name_korea,
            'englishName': obj.name_english,
            'tagList': list(),
            'priceUnit': priceUnit,
            'currentPrice': f"{obj.price:.2f}",
            'dailyChange': f"{obj.price-obj.price_open:.2f}",
            'dailyChangePercentage': f"{(obj.price-obj.price_open)/obj.price_open:.2f}",
            '52weekHigh': f'{weekHigh52["price"]:.2f}',
            '52weekLow': f'{weekLow52["price"]:.2f}',
            "fallingPercentageFrom52WeekHigh": f'{(weekHigh52["price"]- obj.price) / weekHigh52["price"]:.2f}',
        })