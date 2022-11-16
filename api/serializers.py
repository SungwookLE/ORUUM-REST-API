#  file: api/serializers.py
import re
import json

from rest_framework import serializers
from api.models import StockList, StockInformationHistory, StockPriceHistory, StockProfile
from django.core.exceptions import ObjectDoesNotExist


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
    dateArray = serializers.SerializerMethodField() 
    closeArray = serializers.SerializerMethodField() 
    openArray = serializers.SerializerMethodField() 
    highArray = serializers.SerializerMethodField() 
    lowArray = serializers.SerializerMethodField() 
    volumeArray = serializers.SerializerMethodField() 
    
    class Meta:
        model = StockPriceHistory
        fields = ["ticker", "dateArray", "closeArray", "openArray", "highArray", "lowArray", "volumeArray"]

    def get_dateArray(self, object): 
        return object.update_date

    def get_closeArray(self, object): 
        return object.price_close

    def get_openArray(self, object): 
        return object.price_open
    
    def get_highArray(self, object): 
        return object.price_high
    
    def get_lowArray(self, object): 
        return object.price_low
    
    def get_volumeArray(self, object): 
        return object.volume
    

class StockSummarySerializer(serializers.ModelSerializer):
    koreanName = serializers.SerializerMethodField()
    englishName = serializers.SerializerMethodField()
    tagList = serializers.SerializerMethodField()
    priceUnit = serializers.SerializerMethodField()
    currentPrice = serializers.SerializerMethodField()
    dailyChange = serializers.SerializerMethodField()
    dailyChangePercentage = serializers.SerializerMethodField()
    # 
    fiftytwoWeekHigh = serializers.SerializerMethodField() # 52weekHigh 
    fiftytwoWeekLow = serializers.SerializerMethodField() # 52weekLow 
    fallingPercentageFrom52WeekHigh = serializers.SerializerMethodField() 
    ttmPER = serializers.SerializerMethodField() 
    ttmPSR = serializers.SerializerMethodField() 
    ttmPBR = serializers.SerializerMethodField() 
    ttmPEGR = serializers.SerializerMethodField() 
    forwardPER = serializers.SerializerMethodField() 
    forwardPSR = serializers.SerializerMethodField() 
    marketCap = serializers.SerializerMethodField() 
    ttmpEPS = serializers.SerializerMethodField() 
    
    class Meta:
        model = StockList 
        fields = ["ticker", "koreanName", "englishName", "tagList", "priceUnit", "currentPrice", "dailyChange", "dailyChangePercentage", "fiftytwoWeekHigh", "fiftytwoWeekLow", "fallingPercentageFrom52WeekHigh", "ttmPER", "ttmPSR", "ttmPBR", "ttmPEGR", "forwardPER", "forwardPSR", "marketCap", "ttmpEPS"]
    
    def get_koreanName(self, object): 
        return object.name_korea
    
    def get_englishName(self, object): 
        return object.name_english
    
    def get_tagList(self, object): 
        return list()  
    
    def get_priceUnit(self, object): 
        return "dollar" if re.search("^NYSE|^Nasdaq", object.market) else None

    def get_currentPrice(self, object): 
        return f"{object.price:.2f}"

    def get_dailyChange(self, object): 
        return f"{object.price-object.price_open:.2f}"

    def get_dailyChangePercentage(self, object): 
        try: 
            return f"{(object.price-object.price_open)/object.price_open:.2f}"
        except ZeroDivisionError: 
            return 0 

    def get_fiftytwoWeekHigh(self, object): 
        try: 
            return f"{object.stockinformationhistory.fiftytwoweek_high:.2f}" if (object.stockinformationhistory.fiftytwoweek_high is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_fiftytwoWeekLow(self, object): 
        try: 
            return f"{object.stockinformationhistory.fiftytwoweek_low:.2f}" if (object.stockinformationhistory.fiftytwoweek_low is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_fallingPercentageFrom52WeekHigh(self, object): 
        try:        
            return f'{(object.stockinformationhistory.fiftytwoweek_high-object.price) / object.stockinformationhistory.fiftytwoweek_high:.2f}'
        except TypeError: 
            return None 
        except ObjectDoesNotExist: 
            return None
        
    def get_ttmPER(self, object): 
        try:
            return f"{object.stockinformationhistory.ttmPER:.2f}" if (object.stockinformationhistory.ttmPER is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_ttmPSR(self, object): 
        try:
            return f"{object.stockinformationhistory.ttmPSR:.2f}" if (object.stockinformationhistory.ttmPSR is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_ttmPBR(self, object): 
        try:
            return f"{object.stockinformationhistory.ttmPBR:.2f}" if (object.stockinformationhistory.ttmPBR is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_ttmPEGR(self, object): 
        try:
            return f"{object.stockinformationhistory.ttmPEGR:.2f}" if (object.stockinformationhistory.ttmPEGR is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_forwardPER(self, object): 
        try: 
            return f"{object.stockinformationhistory.forwardPER:.2f}" if (object.stockinformationhistory.forwardPER is not None) else None
        except ObjectDoesNotExist: 
            return None    
        
    def get_forwardPSR(self, object): 
        try:
            return f"{object.stockinformationhistory.forwardPSR:.2f}" if (object.stockinformationhistory.forwardPSR is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_marketCap(self, object): 
        try:
            return f"{object.stockinformationhistory.marketCap:.2f}" if (object.stockinformationhistory.marketCap is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    def get_ttmpEPS(self, object): 
        try:
            return f"{object.stockinformationhistory.ttmEPS:.2f}" if (object.stockinformationhistory.ttmEPS is not None) else None
        except ObjectDoesNotExist: 
            return None
        
    
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
    

        