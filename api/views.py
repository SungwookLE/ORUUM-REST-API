# oruum-rest-api/api/views.py

from cgitb import lookup
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from api.serializers import StockListSerializers, StockInformationHistorySerializers, StockPriceHistorySerializers
from api.models import Stock_List, Stock_Information_History, Stock_Price_History

from api.serializers import UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from api.models import User_List, User_Interest, User_Portfolio


class StockPageNumberPagination(PageNumberPagination):
    page_size=10

class Stock_List_ListAPIView(ListAPIView):
    queryset = Stock_List.objects.all()
    serializer_class = StockListSerializers
    pagination_class = StockPageNumberPagination

class Stock_List_RetrieveAPIView(RetrieveAPIView):
    queryset = Stock_List.objects.all()
    lookup_field="ticker"
    serializer_class = StockListSerializers


class Stock_Information_History_ListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializers
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return Stock_Information_History.objects.filter(ticker=self.kwargs["ticker"])

class Stock_Information_Spark_ListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializers
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return Stock_Information_History.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])

class Stock_Information_History_RetrieveAPIView(RetrieveAPIView):
    serializer_class = StockInformationHistorySerializers
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return Stock_Information_History.objects.filter(ticker=self.kwargs["ticker"])
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class Stock_Price_History_ListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializers 
    pagination_class = StockPageNumberPagination 

    def get_queryset(self):
        return Stock_Price_History.objects.filter(ticker=self.kwargs["ticker"])

class Stock_Price_Spark_ListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializers
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return Stock_Price_History.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])

class Stock_Price_History_RetrieveAPIView(RetrieveAPIView):
    serializer_class = StockPriceHistorySerializers
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return Stock_Price_History.objects.filter(ticker=self.kwargs["ticker"])
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserPageNumberPagination(PageNumberPagination):
    page_size=10    


class User_List_ListAPIView(ListAPIView):
    queryset = User_List.objects.all()
    serializer_class = UserListSerializers
    pagination_class = UserPageNumberPagination

class User_List_RetrieveAPIView(RetrieveAPIView):
    queryset = User_List.objects.all()
    lookup_field="id_user"
    serializer_class = UserListSerializers

class User_Interest_ListAPIView(ListAPIView):
    queryset = User_Interest.objects.all()
    serializer_class = UserInterestSerializers
    pagination_class = UserPageNumberPagination

class User_Portfolio_ListAPIView(ListAPIView):
    queryset = User_Portfolio.objects.all()
    serializer_class = UserPortfolioSerializers
    pagination_class = UserPageNumberPagination


### TEST: views.py
"""
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser 

# class my_test2_url(APIView):
#     def get_object(self, ticker, s_date, e_date):
#         try:
#             return Stock_Price_History.objects.filter(ticker=ticker).filter(update_date__range=[s_date, e_date])

#         except Stock_List.DoesNotExist:
#             return JsonResponse({'message': "does not exist"}, status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, ticker, s_date, e_date):
#         this_serializer = StockListSerializers(self.get_object(ticker, s_date, e_date), many=True) 
#         return JsonResponse(this_serializer.data, safe=False) 

# class my_test3_url(APIView):
#     def get(self, request, ticker):
#         try:
#             queryset = Stock_Price_History.objects.filter(ticker=ticker)
#             if queryset.count() == 0:
#                 raise Exception('object count is zero')
#         except Exception as e:
#             return JsonResponse({'message': "does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         this_seiralizer = StockPriceHistorySerializers(queryset, many=True)
#         return JsonResponse(this_seiralizer.data, safe=False)

#     def post(self, request):
#         this_serializer = StockPriceHistorySerializers(data=request.data)
#         if this_serializer.is_valid():
#             this_serializer.save()
#             return JsonResponse(this_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(this_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','DELETE'])
# def my_test_url(request, ticker):
#     # find Stock_List by ticker
#     try:
#         queryset = Stock_List.objects.get(ticker=ticker)

#     except Stock_List.DoesNotExist:
#         return JsonResponse({'message': "does not exist"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET': 
#         this_serializer = StockListSerializers(queryset) 
#         return JsonResponse(this_serializer.data) 
        
#     elif request.method == 'DELETE': 
#         queryset.delete() 
#         return JsonResponse({'message': 'seleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         this_serializer = StockListSerializers(queryset, data=data)
#         if this_serializer.is_valid():
#             this_serializer.save()
#             return JsonResponse(this_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(this_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def my_test_spark(request, ticker, s_date, e_date):
#     try:
#         queryset = Stock_Price_History.objects.filter(ticker=ticker).filter(update_date__range=[s_date, e_date])

#     except Stock_List.DoesNotExist:
#         return JsonResponse({'message': "does not exist"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET': 
#         this_serializer = StockListSerializers(queryset, many=True) 
#         return JsonResponse(this_serializer.data, safe=False) 
"""