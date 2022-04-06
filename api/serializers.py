# oruum-rest-api/api/serializers.py

from rest_framework import serializers
from api.models import StockPrice, StockInformation, StockHistory, StockHistory_TSLA

class StockPriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

class StockInformationSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockInformation
        fields = '__all__'

class StockHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StockHistory
        fields = '__all__'
        abstract = True

class StockHistory_TSLA_Serializers(StockHistorySerializers):
    class Meta:
        model = StockHistory_TSLA
        fields = '__all__'