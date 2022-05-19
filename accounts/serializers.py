#  file: accounts/serializers.py

from rest_framework import serializers
from accounts.models import UserList, UserInterest, UserPortfolio


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserList
        exclude = ['password']


class UserInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class UserPortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'
