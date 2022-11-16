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

        return Response(serializer.data)


class StockSummaryAPIView(RetrieveAPIView):
    serializer_class = StockSummarySerializer 
    
    # queryset = StockList.objects.prefetch_related()
    # lookup_field="ticker"
    def get_queryset(self):
        # return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"]) 
        return StockList.objects.prefetch_related().filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data) 
    
    # def get(self, request, ticker):
    #     obj = self.get_object()

    #     priceUnit = "dollar" if re.search("^NYSE|^Nasdaq", obj.market) else None

        # return Response({
        #     'ticker': obj.ticker,
        #     'koreanName': obj.name_korea,
        #     'englishName': obj.name_english,
        #     'tagList': list(),
        #     'priceUnit': priceUnit,
        #     'currentPrice': f"{obj.price:.2f}",
        #     'dailyChange': f"{obj.price-obj.price_open:.2f}",
        #     'dailyChangePercentage': f"{(obj.price-obj.price_open)/obj.price_open:.2f}",
        #     '52weekHigh': f"{obj.stockinformationhistory.fiftytwoweek_high:.2f}" if (obj.stockinformationhistory.fiftytwoweek_high is not None) else None,
        #     '52weekLow': f"{obj.stockinformationhistory.fiftytwoweek_low:.2f}" if (obj.stockinformationhistory.fiftytwoweek_low is not None) else None,
        #     "fallingPercentageFrom52WeekHigh": f'{(obj.stockinformationhistory.fiftytwoweek_high- obj.price) / obj.stockinformationhistory.fiftytwoweek_high:.2f}',
        #     "ttmPER" : f"{obj.stockinformationhistory.ttmPER:.2f}" if (obj.stockinformationhistory.ttmPER is not None) else None,
        #     "ttmPSR" : f"{obj.stockinformationhistory.ttmPSR:.2f}" if (obj.stockinformationhistory.ttmPSR is not None) else None,
        #     "ttmPBR" : f"{obj.stockinformationhistory.ttmPBR:.2f}" if (obj.stockinformationhistory.ttmPBR is not None) else None,
        #     "ttmPEGR" : f"{obj.stockinformationhistory.ttmPEGR:.2f}" if (obj.stockinformationhistory.ttmPEGR is not None) else None,
        #     "forwardPER" : f"{obj.stockinformationhistory.forwardPER:.2f}" if (obj.stockinformationhistory.forwardPER is not None) else None,
        #     "forwardPSR" : f"{obj.stockinformationhistory.forwardPSR:.2f}" if (obj.stockinformationhistory.forwardPSR is not None) else None,
        #     "marketCap" : f"{obj.stockinformationhistory.marketCap:.2f}" if (obj.stockinformationhistory.marketCap is not None) else None,
        #     "ttmpEPS" : f"{obj.stockinformationhistory.ttmEPS:.2f}" if (obj.stockinformationhistory.ttmEPS is not None) else None
        # })
        

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
