#  file: accounts/urls.py

from django.urls import path, include, register_converter
from accounts.views import KakaoLogoutView, KakaoCallBackView, KakaoView, UserListListAPIView, UserListRetrieveAPIView, UserInterestListAPIView, UserPortfolioListAPIView
from accounts.views import UserInformationView

app_name = 'accounts'

urlpatterns = [
    path('userlist/', UserListListAPIView.as_view(), name='userlist-list'),
    path('userlist/<int:id_user>/',
         UserListRetrieveAPIView.as_view(), name='userlist-detail'),

    path('userinterest/', UserInterestListAPIView.as_view(),
         name='userinterest-list'),
    path('userportfolio/', UserPortfolioListAPIView.as_view(),
         name='userportfolio-list'),

    path('kakao/', KakaoView.as_view()),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('kakao/logout/', KakaoLogoutView.as_view()),

    path('userinformation/<str:id>/<str:token>/', 
          UserInformationView.as_view(), name='userinformation-detail'), # (10/30) access_token을 url 파라미터로 전달하며 노출되게 하는건 올바르지 않음

]
