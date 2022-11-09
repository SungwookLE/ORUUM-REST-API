#  file: accounts/serializers.py

from rest_framework import serializers
from accounts.models import UserList, UserInterest, UserPortfolio, UserWallet


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserList
        fields = ['id', 'email', 'nickname', 'thumbnail_image']


class UserInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class UserPortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'


class UserInformationSerializers(serializers.ModelSerializer): # (11/9) RetrieveAPIView에 serializer_class 없는 경우 에러 해결을 위한 임시방편으로 구성 
    class Meta:
        model = UserWallet
        fields = '__all__'
