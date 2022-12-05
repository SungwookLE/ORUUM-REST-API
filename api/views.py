#  file: api/views.py
import json
import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.serializers import StockListSerializer, StockInformationHistorySerializer, StockPriceHistorySerializer, HistoricalStockPriceSerializer, StockSummarySerializer, StockYearlyFinancialStatementsSerializer, StockQuarterlyFinancialStatementsSerializer, StockProfileSerializer
from api.models import StockList, StockInformationHistory, StockPriceHistory, StockProfile


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
    serializer_class = StockSummarySerializer 
    lookup_field = "ticker"
    
    def get_queryset(self):
        return StockList.objects.prefetch_related().filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data) 


class StockYearlyFinancialStatementsAPIView(RetrieveAPIView): 
    serializer_class = StockYearlyFinancialStatementsSerializer

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data) 


class StockQuarterlyFinancialStatementsAPIView(RetrieveAPIView):
    serializer_class = StockQuarterlyFinancialStatementsSerializer

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data) 


class StockProfileAPIView(RetrieveAPIView):
    serializer_class = StockProfileSerializer

    def get_queryset(self):
        return StockProfile.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data) 
