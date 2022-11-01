#  file: accounts/views.py

from django.http import JsonResponse
from rest_framework.response import Response
import requests  

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.shortcuts import render, redirect
from accounts.serializers import UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from accounts.models import UserList, UserInterest, UserPortfolio
from rest_framework.views import View

from django.contrib import auth
import re

import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    secrets = json.loads(f.read())

class UserPageNumberPagination(PageNumberPagination):
    page_size = 10

# 카카오 로그인 구현/스터디
## (10/25) https://velog.io/@wingnawing/django-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%86%8C%EC%85%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8-api
## (10/26) https://velog.io/@junsikchoi/Django%EB%A1%9C-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%86%8C%EC%85%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8%EC%9D%84-%ED%95%B4%EB%B3%B4%EC%9E%90

class KakaoView(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://0.0.0.0:8000/accounts/kakao/callback/"
        client_id = secrets["KAKAO_REST_API_KEY"]
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

class KakaoCallBackView(View):
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id" : secrets["KAKAO_REST_API_KEY"],
            "redirect_uri": "http://0.0.0.0:8000/accounts/kakao/callback/", 
            "code"      : request.GET["code"]
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        self.access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

        kakako_user_api = "https://kapi.kakao.com/v2/user/me"
        header          = {"Authorization": f"Bearer ${self.access_token}"}
        self.user_information = requests.get(kakako_user_api, headers=header).json()

        self.kakao_signup_login(request)

        return JsonResponse({"access_token": self.access_token, "user_information":self.user_information})

    def kakao_signup_login(self, request):
        try:
            user = UserList.objects.get(id=self.user_information["id"])
            user.kakao_access_token = self.access_token
            user.thumbnail_image = self.user_information["kakao_account"]["profile"]["thumbnail_image_url"]
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except UserList.DoesNotExist:
            UserList.objects.create(id=self.user_information["id"], email=self.user_information["kakao_account"]["email"], nickname=self.user_information["kakao_account"]["profile"]["nickname"], thumbnail_image=self.user_information["kakao_account"]["profile"]["thumbnail_image_url"], kakao_access_token = self.access_token)
            user = UserList.objects.get(id=self.user_information["id"])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return

class KakaoLogoutView(View):
    def get(self, request, id_user):

        # (10/30) 장고 앱에서 발급한 JWT를 비교하여, 어떤 유저의 요청인지 체크하고, 유효한 JWT라면, JWT를 이용하여 ACCESS_TOKEN 얻어서, logout에 넣어주기.
        # (10/31) 유저 데이터베이스에 kakao의 access_token을 저장해둔 다음에, url 파라미터로 유저의 id값을 전달 받으면, 그 값을 가지고 logout 한다.
        # (10/31) JWT를 이용해서 유저 정보를 가져오는게 나으려나???
        try:
            user =UserList.objects.get(id=id_user)
            access_token = user.kakao_access_token
            kakao_logout_api = "https://kapi.kakao.com/v1/user/logout"
            header = {"Authorization": f"Bearer ${access_token}"}
            self.logout_id = requests.post(kakao_logout_api, headers=header).json()
            auth.logout(request)
        except UserList.DoesNotExist:
            return JsonResponse({"Error": "Check the ID"})
        return JsonResponse(self.logout_id)

class UserInformationView(RetrieveAPIView):
    queryset = UserList.objects.prefetch_related()
    lookup_field="id"

    def get(self, request, id):
        obj = self.get_object()
        
        portfolio_koreanStock_list = list()
        portfolio_usStock_list = list()
        for iter_obj in obj.userportfolio.all():
            portfolio_koreanStock_dict = dict()
            portfolio_usStock_dict = dict()

            if re.search(r".KS$",str(iter_obj.ticker)):
                portfolio_koreanStock_dict["ticker"] = str(iter_obj.ticker)
                portfolio_koreanStock_dict["number"] = str(iter_obj.number_stock)
                portfolio_koreanStock_list.append(portfolio_koreanStock_dict)
            else:
                portfolio_usStock_dict["ticker"] = [str(iter_obj.ticker)]
                portfolio_usStock_dict["number"] = str(iter_obj.number_stock)
                portfolio_usStock_list.append(portfolio_usStock_dict)

        
        interest_koreanStock_list = list()
        interest_usStock_list = list()
        for iter_obj in obj.userinterest.all():
            interest_koreanStock_dict = dict()
            interest_usStock_dict = dict()
            if re.search(r".KS$",str(iter_obj.ticker)):
                interest_koreanStock_dict["ticker"]= [str(iter_obj.ticker)] 
                interest_koreanStock_list.append(interest_koreanStock_dict)
            else:
                interest_usStock_dict["ticker"] = [str(iter_obj.ticker)] 
                interest_usStock_list.append(interest_usStock_dict)

        return Response({
            "nickname": obj.nickname,
            "portfolio_koreanStock": portfolio_koreanStock_list, 
            "interest_koreanStock": interest_koreanStock_list,
            "portfolio_usStock": portfolio_usStock_list,
            "interest_usStock": interest_usStock_list,
            "deposit": obj.userwallet.deposit 
        })



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
