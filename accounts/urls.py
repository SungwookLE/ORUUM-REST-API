#  file: accounts/urls.py

from django.urls import path, include, register_converter
from rest_framework import routers
from accounts.views import UserListListAPIView, UserListRetrieveAPIView, UserInterestListAPIView, UserPortfolioListAPIView

app_name = 'accounts'

urlpatterns = [
    path('userlist/', UserListListAPIView.as_view(), name='userlist-list'),
    path('userlist/<int:id_user>/',
         UserListRetrieveAPIView.as_view(), name='userlist-detail'),

    path('userinterest/', UserInterestListAPIView.as_view(),
         name='userinterest-list'),
    path('userportfolio/', UserPortfolioListAPIView.as_view(),
         name='userportfolio-list'),
]
