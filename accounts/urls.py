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

    path('userinformation/<int:id_user>/', 
          UserInformationView.as_view(), name='userinformation-detail'), 


    # https://velog.io/@junsikchoi/Django%EB%A1%9C-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%86%8C%EC%85%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8%EC%9D%84-%ED%95%B4%EB%B3%B4%EC%9E%90
    path('kakao/login/', KakaoView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('kakao/logout/', KakaoLogoutView.as_view(), name='kakao-logout'),

    
    # (11/1) simple-jwt 구현 
    path('jwt/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
