#  file: api/serializers.py


from rest_framework import serializers
from api.models import StockList, StockInformationHistory, StockPriceHistory


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockList
        fields = '__all__'


class StockInformationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInformationHistory
        fields = '__all__'


class StockPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPriceHistory
        fields = '__all__'

class HistoricalStockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPriceHistory
        fields = ["ticker", "update_date", "price_close", "price_open","price_high","price_low", "volume"]