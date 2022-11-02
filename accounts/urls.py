#  file: accounts/urls.py

from django.urls import path
from accounts.views import KakaoLogoutView, KakaoCallBackView, KakaoView, UserListListAPIView, UserListRetrieveAPIView, UserInterestListAPIView, UserPortfolioListAPIView
from accounts.views import UserInformationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)


app_name = 'accounts'

urlpatterns = [
    path('userlist/', UserListListAPIView.as_view(), name='userlist-list'),
    path('userlist/<int:id_user>/',
         UserListRetrieveAPIView.as_view(), name='userlist-detail'),

    path('userinterest/', UserInterestListAPIView.as_view(),
         name='userinterest-list'),
    path('userportfolio/', UserPortfolioListAPIView.as_view(),
         name='userportfolio-list'),

    path('kakao/', KakaoView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('kakao/logout/<int:id_user>/', KakaoLogoutView.as_view()),

    path('userinformation/<str:id>/', 
          UserInformationView.as_view(), name='userinformation-detail'), # (10/30) access_token을 url 파라미터로 전달하며 노출되게 하는건 올바르지 않음

    # (11/1) simple-jwt 구현 
    path('jwt-token-auth/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('jwt-token-auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt-token-auth/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
