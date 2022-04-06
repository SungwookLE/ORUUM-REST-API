from tabnanny import verbose
from turtle import update
from django.db import models
from django.urls import reverse
from datetime import datetime

class StockPrice(models.Model): # 오늘의 주식 가격과 전종목 리스트
    symbol = models.CharField(verbose_name='symbol', max_length=30, primary_key=True, blank=False, default='')
    name = models.CharField(verbose_name='name', max_length=50,blank=False, default='')
    market = models.CharField(verbose_name='market', max_length=50,blank=False, default='')
    
    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    price = models.FloatField(verbose_name='price', blank=False, default=0)
    open = models.FloatField(verbose_name='open', blank=False, default=0)
    prevclose = models.FloatField(verbose_name='prevclose', blank=False, default=0)
    high = models.FloatField(verbose_name='high', blank=False, default=0)
    low = models.FloatField(verbose_name='low', blank=False, default=0)
    volume = models.FloatField(verbose_name='volume', blank=False, default=0)

    date = models.DateField(verbose_name='date', blank=False, help_text='날짜', default=datetime.today) 

    def __str__(self): 
        return self.symbol


class StockInformation(models.Model): # 오늘의 주식 정보(전종목)
    symbol = models.OneToOneField("StockPrice", related_name="stockinformation", on_delete=models.CASCADE, db_column = "symbol", primary_key=True)
    
    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)
    
    total_assets = models.FloatField(verbose_name='total_assets', blank=False, default=0, help_text='자산총계')
    curruent_assets =  models.FloatField(verbose_name='curruent_assets', blank=False, default=0, help_text='유동자산')
    inventory = models.FloatField(verbose_name='inventory', blank=False, default=0, help_text='재고자산')
    quick_assets = models.FloatField(verbose_name='quick_assets', blank=False, default=0, help_text='당좌자산')
    non_current_assets = models.FloatField(verbose_name='non_current_assets', blank=False, default=0, help_text='비유동자산')
    investments = models.FloatField(verbose_name='investments', blank=False, default=0, help_text='투자자산')
    tagible_assets = models.FloatField(verbose_name='tagible_assets', blank=False, default=0, help_text='유형자산')
    liabilities = models.FloatField(verbose_name='liabilities', blank=False, default=0, help_text='부채')
    current_liabilities = models.FloatField(verbose_name='current_liabilities', blank=False, default=0, help_text='유동부채')
    non_current_liabilities = models.FloatField(verbose_name='non_current_liabilities', blank=False, default=0, help_text='비유동부채')
    total_assets_ratio = models.FloatField(verbose_name='total_assets_ratio', blank=False, default=0, help_text='유동비율')
    quick_assets_ratio = models.FloatField(verbose_name='quick_assets_ratio', blank=False, default=0, help_text='당좌비율')
    liabilities_ratio = models.FloatField(verbose_name='liabilities_ratio', blank=False, default=0, help_text='부채비율')
    total_revenue = models.FloatField(verbose_name='total_revenue', blank=False, default=0, help_text='매출액')
    gross_profit = models.FloatField(verbose_name='gross_profit', blank=False, default=0, help_text='매출총이익')
    operating_income = models.FloatField(verbose_name='operating_income', blank=False, default=0, help_text='영업이익')
    net_income = models.FloatField(verbose_name='net_income', blank=False, default=0, help_text='순이익')
    total_revenue_ratio = models.FloatField(verbose_name='total_revenue_ratio', blank=False, default=0, help_text='매출이익률')
    operating_income_ratio = models.FloatField(verbose_name='operating_income_ratio', blank=False, default=0, help_text='영업이익률')
    net_income_ratio = models.FloatField(verbose_name='net_income_ratio', blank=False, default=0, help_text='순이익률')
    operating_cash_flow = models.FloatField(verbose_name='operating_cash_flow', blank=False, default=0, help_text='영업현금흐름')

    date = models.DateField(verbose_name='date', blank=False, help_text='날짜', default=datetime.today)

    def __str__(self): 
        return str(self.symbol)


# Below: StockHistory Model
class StockHistory(models.Model): # 모든 종목의 상장 이후 ~ 현재일까지의 주가가 기록된 테이블

    #id : primary key
    symbol = models.ForeignKey("StockPrice", related_name="stockhistory", on_delete=models.CASCADE, db_column = "symbol")
    date = models.DateField(verbose_name='date', blank=False, help_text='날짜', default=datetime.today)
    
    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)
    
    splits = models.FloatField(verbose_name='spits',null=True, blank=True, help_text='주식분할 내역')
    dividends = models.FloatField(verbose_name='dividends',null=True, blank=True, help_text='배당 내역')

    opens = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="개장가")
    high = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="고가")
    low = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="저가")
    close = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="종가")
    adj_close = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="조정 종가")
    volume = models.FloatField(verbose_name='opens', blank=False, default=0, help_text="거래량")

    def __str__(self): 
        return str(self.symbol)
