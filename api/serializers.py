#  file: api/serializers.py


from rest_framework import serializers
from api.models import StockList, StockInformationHistory, StockPriceHistory, StockProfile


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

# (10/03) API 요구사항 반영을 위한 신규 REST serializer 생성1
class StockYearlyFinancialStatementsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = StockInformationHistory
        fields = '__all__'

# (10/19) API 요구사항 반영을 위한 신규 REST serializer 생성2
class StockProfileSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = StockProfile
        fields = '__all__'
        
class StockQuarterlyFinancialStatementsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = StockInformationHistory
        fields = '__all__'
        