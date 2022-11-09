#  file: accounts/urls.py

from django.urls import path

from accounts.views import (KakaoLogoutView, KakaoCallBackView, KakaoView, UserListListAPIView, 
          UserListRetrieveAPIView, UserInterestListAPIView, UserPortfolioListAPIView)
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

     # (10/26) 카카오 로그인 구현/스터디
     # https://velog.io/@junsikchoi/Django%EB%A1%9C-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%86%8C%EC%85%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8%EC%9D%84-%ED%95%B4%EB%B3%B4%EC%9E%90

    path('kakao/', KakaoView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('kakao/logout/<int:id_user>/', KakaoLogoutView.as_view()),

    # (11/3) 쿠키에서 JWT를 받아서 유저 인증하고 해당하는 유저의 userinformation을 보여주는 방식으로 바꾸기
    path('userinformation/<str:id>/', 
          UserInformationView.as_view(), name='userinformation-detail'), 

    # (11/1) simple-jwt 구현 
    path('jwt-token-auth/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('jwt-token-auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt-token-auth/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
