#  file: accounts/views.py

from cgitb import lookup
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.shortcuts import render
from accounts.serializers import UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from accounts.models import UserList, UserInterest, UserPortfolio


class UserPageNumberPagination(PageNumberPagination):
    page_size = 10


class UserListListAPIView(ListAPIView):
    queryset = UserList.objects.all()
    serializer_class = UserListSerializers
    pagination_class = UserPageNumberPagination


class UserListRetrieveAPIView(RetrieveAPIView):
    queryset = UserList.objects.all()
    lookup_field = "id_user"
    serializer_class = UserListSerializers


class UserInterestListAPIView(ListAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializers
    pagination_class = UserPageNumberPagination


class UserPortfolioListAPIView(ListAPIView):
    queryset = UserPortfolio.objects.all()
    serializer_class = UserPortfolioSerializers
    pagination_class = UserPageNumberPagination
