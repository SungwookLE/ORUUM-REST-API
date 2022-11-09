#  file: accounts/views.py

import os
import re
import json
import requests

from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import View, APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.serializers import UserInformationSerializers, UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from accounts.models import UserList, UserInterest, UserPortfolio


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    secrets = json.loads(f.read())


class UserPageNumberPagination(PageNumberPagination):
    page_size = 10

class KakaoView(APIView): # View -> APIView 
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://0.0.0.0:8000/accounts/kakao/callback/"
        client_id = secrets["KAKAO_REST_API_KEY"]
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

class KakaoCallBackView(APIView):
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id": secrets["KAKAO_REST_API_KEY"],
            "redirect_uri": "http://0.0.0.0:8000/accounts/kakao/callback/",
            "code": request.GET["code"]
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        self.kakao_access_token = requests.post(
            kakao_token_api, data=data).json()["access_token"]

        dict_user_kakao, user = self.get_user_as_dict_with_kakao_login(request)
        dict_jwt = self.get_jwt_login(user)
        dict_user_kakao.update(dict_jwt)

        response = Response(dict_user_kakao,
                            status=status.HTTP_200_OK
                            )

        response.set_cookie("jwt_access_token",
                            dict_jwt["jwt_access_token"], httponly=True)
        response.set_cookie("jwt_refresh_token",
                            dict_jwt["jwt_refresh_token"], httponly=True)

        return response

    def get_user_as_dict_with_kakao_login(self, request):
        ret = dict()

        kakako_user_api = "https://kapi.kakao.com/v2/user/me"
        header = {"Authorization": f"Bearer ${self.kakao_access_token}"}
        self.user_information = requests.get(
            kakako_user_api, headers=header).json()

        kakao_id = self.user_information["id"]
        kakao_email = self.user_information["kakao_account"]["email"]
        kakao_nickname = self.user_information["kakao_account"]["profile"]["nickname"]
        kakao_thumbnail_image = self.user_information["kakao_account"]["profile"]["thumbnail_image_url"]

        try:
            user = UserList.objects.get(id=kakao_id)
            user.kakao_access_token = self.kakao_access_token
            user.thumbnail_image = kakao_thumbnail_image
            user.nickname = kakao_nickname
            user.email = kakao_email
            user.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
        except UserList.DoesNotExist:
            UserList.objects.create(id=kakao_id, email=kakao_email, nickname=kakao_nickname,
                                    thumbnail_image=kakao_thumbnail_image, kakao_access_token=self.kakao_access_token)
            user = UserList.objects.get(id=kakao_id)
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')

        ret["user_oruum"] = UserListSerializers(user).data

        return ret, user

    def get_jwt_login(self, user):
        ret = dict()

        jwt_token = TokenObtainPairSerializer.get_token(user)
        jwt_refresh_token = str(jwt_token)
        jwt_access_token = str(jwt_token.access_token)

        ret = {
            "jwt_access_token": jwt_access_token,
            "jwt_refresh_token": jwt_refresh_token
        }

        return ret


class KakaoLogoutView(APIView): # View -> APIView 
    def get(self, request, id_user):

        # (10/30) 장고 앱에서 발급한 JWT를 비교하여, 어떤 유저의 요청인지 체크하고, 유효한 JWT라면, JWT를 이용하여 ACCESS_TOKEN 얻어서, logout에 넣어주기.
        # (10/31) 유저 데이터베이스에 kakao의 access_token을 저장해둔 다음에, url 파라미터로 유저의 id값을 전달 받으면, 그 값을 가지고 logout 한다.
        # (10/31) JWT를 이용해서 유저 정보를 가져오는게 나으려나???
        try:
            user = UserList.objects.get(id=id_user)
            access_token = user.kakao_access_token
            kakao_logout_api = "https://kapi.kakao.com/v1/user/logout"
            header = {"Authorization": f"Bearer ${access_token}"}
            self.logout_id = requests.post(
                kakao_logout_api, headers=header).json()
            auth.logout(request)
        except UserList.DoesNotExist:
            return JsonResponse({"Error": "Check the ID"})
        return JsonResponse(self.logout_id)


class UserInformationView(RetrieveAPIView):
    queryset = UserList.objects.prefetch_related()
    lookup_field = "id"
    # serializer_class = UserInformationSerializers

    def get(self, request, id):
        obj = self.get_object()

        portfolio_koreanStock_list = list()
        portfolio_usStock_list = list()
        for iter_obj in obj.userportfolio.all():
            portfolio_koreanStock_dict = dict()
            portfolio_usStock_dict = dict()

            if re.search(r".KS$", str(iter_obj.ticker)):
                portfolio_koreanStock_dict["ticker"] = str(iter_obj.ticker)
                portfolio_koreanStock_dict["number"] = str(
                    iter_obj.number_stock)
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
            if re.search(r".KS$", str(iter_obj.ticker)):
                interest_koreanStock_dict["ticker"] = [str(iter_obj.ticker)]
                interest_koreanStock_list.append(interest_koreanStock_dict)
            else:
                interest_usStock_dict["ticker"] = [str(iter_obj.ticker)]
                interest_usStock_list.append(interest_usStock_dict)
        try:
            deposit = obj.userwallet.deposit
        except ObjectDoesNotExist:
            deposit = ""

        return Response({
            "nickname": obj.nickname,
            "portfolio_koreanStock": portfolio_koreanStock_list,
            "interest_koreanStock": interest_koreanStock_list,
            "portfolio_usStock": portfolio_usStock_list,
            "interest_usStock": interest_usStock_list,
            "deposit": deposit
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
