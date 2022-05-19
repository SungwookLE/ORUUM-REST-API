#  file: api/serializers.py


from rest_framework import serializers
from api.models import StockList, StockInformationHistory, StockPriceHistory


class StockListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockList
        fields = '__all__'


class StockInformationHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StockInformationHistory
        fields = '__all__'


class StockPriceHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StockPriceHistory
        fields = '__all__'
