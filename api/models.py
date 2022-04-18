from tabnanny import verbose
from turtle import update
from django.db import models
from django.urls import reverse
from datetime import datetime


class User_List(models.Model): # 모든 유저 회원정보, oAuth 연계
    id_user = models.BigAutoField(help_text="id_user_list", primary_key=True)
    email_address = models.CharField(verbose_name='email_address', max_length=50,blank=False, default='', help_text='메일주소', unique=True)
    first_name = models.CharField(verbose_name='first_name', max_length=50,blank=False, default='', help_text='이름')
    last_name = models.CharField(verbose_name='last_name', max_length=50,blank=False, default='', help_text='성')

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    def __str__(self): 
        return str(self.id_user)
    
    def get_absolute_url(self):
        return reverse('user_list-detail', args=(self.id_user))


class User_Interest(models.Model): # 모든 유저의 유저별 관심종목
    id = models.BigAutoField(help_text="id_user_interest", primary_key=True)
    id_user = models.ForeignKey("User_List", related_name="user_interest", on_delete=models.CASCADE, db_column = "id_user")
    ticker = models.ForeignKey("Stock_List", related_name="user_interest", on_delete=models.CASCADE, db_column = "ticker")

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    def __str__(self): 
        return str(self.id)


class User_Portfolio(models.Model): # 모든 유저의 유저별 포트폴리오
    id = models.BigAutoField(help_text="id_user_portfolio", primary_key=True)
    id_user = models.ForeignKey("User_List", related_name="user_portfolio", on_delete=models.CASCADE, db_column = "id_user")
    ticker = models.ForeignKey("Stock_List", related_name="user_portfolio", on_delete=models.CASCADE, db_column = "ticker")
    number_stock = models.IntegerField(verbose_name='number_stock', blank=False, default=0, help_text='보유수량')
    average_price = models.FloatField(verbose_name='average_price', blank=False, default=0, help_text='평균매입가')
    price_earning_ratio = models.FloatField(verbose_name='price_earning_ratio', blank=False, default=0, help_text='주가수익률')
    price_return_won = models.FloatField(verbose_name='price_return_won', blank=False, default=0, help_text='수익금(원)')
    price_return_dollar = models.FloatField(verbose_name='price_return_dollar', blank=False, default=0, help_text='수익금(달러)')

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    def __str__(self): 
        return str(self.id)


class Stock_List(models.Model): # 오늘의 주식 가격과 전종목 리스트
    ticker = models.CharField(verbose_name='ticker', primary_key=True , max_length=50, blank=False, null=False, default='', help_text="Ticker(Symbol)")
    update_day = models.DateField(verbose_name='update_day', blank=False, help_text='업데이트 날짜', default=datetime.today) 
    name_english = models.CharField(verbose_name='name_english', max_length=50,blank=False, default='', help_text='주식명(영어)')
    name_korea = models.CharField(verbose_name='name_korea', max_length=50,blank=False, default='', help_text='주식명(한국어)')
    market = models.CharField(verbose_name='market', max_length=50,blank=False, default='', help_text='상장사')
    price = models.FloatField(verbose_name='price', blank=False, default=0, help_text='주가')
    price_open = models.FloatField(verbose_name='price_open', blank=False, default=0, help_text='시가')
    prevclose = models.FloatField(verbose_name='prevclose', blank=False, default=0, help_text='전일가')
    price_high = models.FloatField(verbose_name='price_high', blank=False, default=0, help_text='고가')
    price_low = models.FloatField(verbose_name='price_low', blank=False, default=0, help_text='저가')
    volume = models.FloatField(verbose_name='volume', blank=False, default=0, help_text='거래량')

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    def __str__(self): 
        return str(self.ticker)

    def get_absolute_url(self):
        return reverse('stock_list-detail', args=(self.ticker))


class Stock_Information_History(models.Model): # 그 동안의 주식 실적 정보(전종목)
    id = models.BigAutoField(help_text="id_stock_information_history", primary_key=True)
    ticker = models.ForeignKey("Stock_List", related_name="stock_information_history", on_delete=models.CASCADE, db_column = "ticker")

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

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)

    def __str__(self): 
        return str(self.id)

    # def get_absolute_url(self):
    #     return reverse('stock_information_history-detail', args=(self.ticker))


class Stock_Price_History(models.Model): # 모든 종목의 상장 이후 ~ 현재일까지의 주가가 기록된 테이블

    id = models.BigAutoField(help_text="id_stock_price_history", primary_key=True)
    ticker = models.ForeignKey("Stock_List", related_name="stock_price_history", on_delete=models.CASCADE, db_column = "ticker")
    update_day = models.DateField(verbose_name='update_day', blank=False, help_text='날짜', default=datetime.today)
    
    price_open = models.FloatField(verbose_name='price_open', blank=False, default=0, help_text="시가")
    price_high = models.FloatField(verbose_name='price_high', blank=False, default=0, help_text="고가")
    price_low = models.FloatField(verbose_name='price_low', blank=False, default=0, help_text="저가")
    price_close = models.FloatField(verbose_name='price_close', blank=False, default=0, help_text="종가")
    adj_close = models.FloatField(verbose_name='adj_close', blank=False, default=0, help_text="조정 종가")
    volume = models.FloatField(verbose_name='volume', blank=False, default=0, help_text="거래량")

    splits = models.FloatField(verbose_name='spits',null=True, blank=True, help_text='주식분할 내역')
    dividends = models.FloatField(verbose_name='dividends',null=True, blank=True, help_text='배당 내역')

    update_dt = models.DateTimeField(verbose_name='update_dt', blank=False, auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', blank=False, auto_now_add=True)
    
    def __str__(self): 
        return str(self.id)

    # def get_absolute_url(self):
    #     return reverse('stock_price_history-detail', args=(self.ticker))