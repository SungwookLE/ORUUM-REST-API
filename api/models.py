from tabnanny import verbose
from django.db import models
from django.urls import reverse

class StockPrice(models.Model):
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

    def __str__(self): 
        return self.symbol


class StockInformation(models.Model):
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

    def __str__(self): 
        return str(self.symbol)
