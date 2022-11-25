#  file: accounts/views.py

from django.http import JsonResponse
from rest_framework.response import Response
import requests
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.shortcuts import render, redirect
from accounts.serializers import UserListSerializers, UserInterestSerializers, UserPortfolioSerializers
from accounts.models import UserList, UserInterest, UserPortfolio
from rest_framework.views import View, APIView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken, TokenVerifySerializer
import os
import json
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    secrets = json.loads(f.read())


class UserPageNumberPagination(PageNumberPagination):
    page_size = 10


class KakaoView(APIView):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://0.0.0.0:8000/accounts/kakao/callback/"
        client_id = secrets["KAKAO_REST_API_KEY"]
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoCallBackView(View):
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

        user = self.login_kakao()
        jwt_token = self.get_jwt(user)

        response = JsonResponse({
                        "user": UserListSerializers(user).data,
                        "access_token": jwt_token["access_token"],
                        "refresh_token": jwt_token["refresh_token"]},
                        status=status.HTTP_200_OK
                        )

        response.set_cookie("oruum_access_token",
                            jwt_token["access_token"], httponly=True)

        return response

    def login_kakao(self):
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
            user.username = kakao_nickname
            user.email = kakao_email
            user.save()

        except UserList.DoesNotExist:
            UserList.objects.create(id=kakao_id, email=kakao_email, username=kakao_nickname,
                                    thumbnail_image=kakao_thumbnail_image, kakao_access_token=self.kakao_access_token)
            user = UserList.objects.get(id=kakao_id)
     
        return user

    def get_jwt(self, user):
        jwt_token = RefreshToken.for_user(user)
        jwt_refresh_token = str(jwt_token)
        jwt_access_token = str(jwt_token.access_token)

     
        ret = {
            "access_token": jwt_access_token,
            "refresh_token": jwt_refresh_token
        }
        
        return ret


class KakaoLogoutView(APIView):
    def get(self, request):
        access_token=request.COOKIES.get('oruum_access_token')
        try:
            # jwt 토큰 검증 with secret KEY
            payload = jwt.decode(access_token, secrets["django_config"]["SECRET_KEY"], algorithms=['HS256'])
        except:
            response = JsonResponse({"message" : "Logout false", "user_oruum": {}},
                            status=status.HTTP_200_OK
                            )
            return response

        user = UserList.objects.get(id=payload["user_id"])
        access_token = user.kakao_access_token

        kakao_logout_api = "https://kapi.kakao.com/v1/user/logout"
        header = {"Authorization": f"Bearer ${access_token}"}
        self.logout_id = requests.post(
                kakao_logout_api, headers=header).json()

        response = JsonResponse({"message" : "Logout success", "user_oruum": UserListSerializers(user).data},
                            status=status.HTTP_200_OK
                            )

        response.delete_cookie("oruum_access_token")
        return response


class UserInformationView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = UserList.objects.prefetch_related()
    lookup_field = "id"
    
    def get(self, request, id):
        header = request.headers.get('Authorization', None)
        access_token = re.split(' ', header)[1]
        # jwt 토큰 검증 with secret KEY
        payload = jwt.decode(access_token, secrets["django_config"]["SECRET_KEY"], algorithms=['HS256']) 
        id_jwt = payload["user_id"]
        
        #############################################################################
        # (11/23) 이런식으로 가지고 있는 토큰이, 조회 요청한 id와 동일한지 체크함
        # 또는 해당 api 자체를 가지고 있는 토큰을 이용해서 유저의 정보를 보여주는 것으로 바꿔줄 수 있겠음, 
        # 현재는 url 파라미터로 유저의 id를 받고 있음
        #############################################################################
        
        if (str(id) == str(id_jwt)):
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
                "username": obj.username,
                "portfolio_koreanStock": portfolio_koreanStock_list,
                "interest_koreanStock": interest_koreanStock_list,
                "portfolio_usStock": portfolio_usStock_list,
                "interest_usStock": interest_usStock_list,
                "deposit": deposit
            })
        else:
            return Response({"Denied": f"your token don't have authority to retrieve the request id {id}"})


class UserListListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,) 
    # http 0.0.0.0:8000/accounts/userlist/ "Authorization: Bearer {access_token}"
    queryset = UserList.objects.all()
    serializer_class = UserListSerializers
    pagination_class = UserPageNumberPagination


class UserListRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,) 
    # http 0.0.0.0:8000/accounts/userlist/ "Authorization: Bearer {access_token}"
    queryset = UserList.objects.all()
    lookup_field = "id_user"
    serializer_class = UserListSerializers


class UserInterestListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,) 
    # http 0.0.0.0:8000/accounts/userlist/ "Authorization: Bearer {access_token}"
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializers
    pagination_class = UserPageNumberPagination


class UserPortfolioListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = UserPortfolio.objects.all()
    serializer_class = UserPortfolioSerializers
    pagination_class = UserPageNumberPagination
