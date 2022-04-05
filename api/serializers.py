# oruum-rest-api/api/serializers.py

from rest_framework import serializers
from api.models import StockPrice, StockInformation

class StockPriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

class StockInformationSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockInformation
        fields = '__all__'