#  file: api/serializers.py
from rest_framework import serializers
from api.models import StockList, StockInformationHistory, StockPriceHistory, StockProfile

import re
import json

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
    # field 추가 
    # company_officers 에서 아래 field에 해당하는 값들을 채워넣음. 
    # serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # title = serializers.SerializerMethodField()
    # pay = serializers.SerializerMethodField()
    # age = serializers.SerializerMethodField()
    # detailList = []
    
    class Meta: 
        model = StockProfile
        fields =  '__all__' # ["name"] name, title, pay, age, detailList
    
    def get_name(self, object): 
        company_officers = object.company_officers 
 
        iter_dict = json.loads(company_officers)
        print(iter_dict) 
        ceo_idx = []
        
        for idx in range(len(iter_dict)): 
            if re.search("CEO", iter_dict[idx]["title"], re.I): ceo_idx.append(idx) 
        try: 
            return [iter_dict[idx]["name"] for idx in ceo_idx] 
        except KeyError: 
            return None 

    # def get_title(self, object) 
    #   company_officers = object.company_officers 
    #   (ceo name을 찾는 로직 추가)
    
    # def get_pay(self, object) 
    #   company_officers = object.company_officers 
    #   (ceo name을 찾는 로직 추가)
    
    # def get_age(self, object) 
    #   company_officers = object.company_officers 
    #   (ceo name을 찾는 로직 추가)
    
class StockQuarterlyFinancialStatementsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = StockInformationHistory
        fields = '__all__'
        