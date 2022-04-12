# oruum-rest-api/api/serializers.py

from rest_framework import serializers
from api.models import Stock_List, Stock_Information_History, Stock_Price_History


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

