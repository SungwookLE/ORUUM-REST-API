#  file: api/serializers.py
import re
import json

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
    dateArray = serializers.SerializerMethodField()
    revenueArray = serializers.SerializerMethodField()
    costOfRevenueArray = serializers.SerializerMethodField()
    grossProfit = serializers.SerializerMethodField()
    operatingExpense = serializers.SerializerMethodField()
    operatingIncome = serializers.SerializerMethodField()
    basicEpsArray = serializers.SerializerMethodField()
    dilutedEpsArray = serializers.SerializerMethodField()
    
    class Meta: 
        model = StockInformationHistory
        fields = ["dateArray", "revenueArray", "costOfRevenueArray", "grossProfit", "operatingExpense", "operatingIncome", "basicEpsArray", "dilutedEpsArray"]
        
    def get_dateArray(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict.keys() 
        except KeyError: 
            return None
        
    def get_revenueArray(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["totalRevenue"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_costOfRevenueArray(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["costOfRevenue"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_grossProfit(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["grossProfit"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_operatingExpense(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["totalOperatingExpenses"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_operatingIncome(self, object): 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["operatingIncome"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_basicEpsArray(self, object): # ttmEPS 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict["ttmEPS"]
        except KeyError: 
            return None
    
    def get_dilutedEpsArray(self, object): # ttmEPS 
        iter_dict = json.loads(object.yearly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict["ttmEPS"]
        except KeyError: 
            return None
        

class StockQuarterlyFinancialStatementsSerializer(serializers.ModelSerializer): 
    dateArray = serializers.SerializerMethodField()
    revenueArray = serializers.SerializerMethodField()
    costOfRevenueArray = serializers.SerializerMethodField()
    grossProfit = serializers.SerializerMethodField()
    operatingExpense = serializers.SerializerMethodField()
    operatingIncome = serializers.SerializerMethodField()
    basicEpsArray = serializers.SerializerMethodField()
    dilutedEpsArray = serializers.SerializerMethodField()
    
    class Meta: 
        model = StockInformationHistory
        fields = ["dateArray", "revenueArray", "costOfRevenueArray", "grossProfit", "operatingExpense", "operatingIncome", "basicEpsArray", "dilutedEpsArray"]
        
    def get_dateArray(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict.keys() 
        except KeyError: 
            return None
        
    def get_revenueArray(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["totalRevenue"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_costOfRevenueArray(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["costOfRevenue"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_grossProfit(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["grossProfit"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_operatingExpense(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["totalOperatingExpenses"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_operatingIncome(self, object): 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return [iter_dict[key]["operatingIncome"] for key in iter_dict.keys()] 
        except KeyError: 
            return None
        
    def get_basicEpsArray(self, object): # ttmEPS 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict["ttmEPS"]
        except KeyError: 
            return None
    
    def get_dilutedEpsArray(self, object): # ttmEPS 
        iter_dict = json.loads(object.quarterly_income_statement)
        try: 
            iter_dict = {key:iter_dict[key] for key in sorted(iter_dict)} 
            return iter_dict["ttmEPS"]
        except KeyError: 
            return None
        
    
# (10/19) API 요구사항 반영을 위한 신규 REST serializer 생성2
class StockProfileSerializer(serializers.ModelSerializer): 
    name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    pay = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    detailList = serializers.SerializerMethodField()
    
    class Meta: 
        model = StockProfile
        fields =  ["name", "title", "pay", "age", "detailList"]
    
    def get_name(self, object): 
        company_officers = object.company_officers 
 
        iter_dict = json.loads(company_officers)
        ceo_idx = []
        
        for idx in range(len(iter_dict)): 
            if re.search("CEO", iter_dict[idx]["title"], re.I): ceo_idx.append(idx) 
        try: 
            return [iter_dict[idx]["name"] for idx in ceo_idx] 
        except KeyError: 
            return None 

    def get_title(self, object): 
        company_officers = object.company_officers 
 
        iter_dict = json.loads(company_officers)
        ceo_idx = []
        
        for idx in range(len(iter_dict)): 
            if re.search("CEO", iter_dict[idx]["title"], re.I): ceo_idx.append(idx) 
        try: 
            return [iter_dict[idx]["title"] for idx in ceo_idx] 
        except KeyError: 
            return None 
    
    def get_pay(self, object): 
        company_officers = object.company_officers 
 
        iter_dict = json.loads(company_officers)
        ceo_idx = []
        
        for idx in range(len(iter_dict)): 
            if re.search("CEO", iter_dict[idx]["title"], re.I): ceo_idx.append(idx) 
        try: 
            return [iter_dict[idx]["totalPay"] for idx in ceo_idx] 
        except KeyError: 
            return None 
    
    def get_age(self, object): 
        company_officers = object.company_officers 
 
        iter_dict = json.loads(company_officers)
        ceo_idx = []
        
        for idx in range(len(iter_dict)): 
            if re.search("CEO", iter_dict[idx]["title"], re.I): ceo_idx.append(idx) 
        try: 
            return [iter_dict[idx]["age"] for idx in ceo_idx] 
        except KeyError: 
            return None 
    
    def get_detailList(self, object): 
        return [] 
    

        