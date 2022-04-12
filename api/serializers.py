# oruum-rest-api/api/serializers.py

from rest_framework import serializers
from api.models import Stock_List, Stock_Information_History, Stock_Price_History, User_List
from api.models import User_List, User_Interest, User_Portfolio


class StockListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock_List
        fields = '__all__'

class StockInformationHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock_Information_History
        fields = '__all__'

class StockPriceHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock_Price_History
        fields = '__all__'

class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_List
        fields = '__all__'

class UserInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_Interest
        fields = '__all__'

class UserPortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_Portfolio
        fields = '__all__'

