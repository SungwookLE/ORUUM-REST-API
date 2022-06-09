#  file: api/models.py


from django.db import models
from django.urls import reverse
from datetime import datetime

class StockList(models.Model): 
    """ 오늘의 주식 가격과 전종목 리스트
    pk = "ticker"
    columns = ["update_date", "name_english", "name_korea", "market", "price", "price_open", "prevclose", "price_high", "price_low", "volume", "update_dt", "create_dt"]
    """

    ticker = models.CharField(primary_key=True , max_length=20, help_text="Ticker(Symbol)")
    update_date = models.DateField(help_text='업데이트 날짜', default=datetime.today) 

    name_english = models.CharField(max_length=50, default='', help_text='주식명(영어)')
    name_korea = models.CharField(max_length=50, blank=True, null=True, help_text='주식명(한국어)')

    market = models.CharField(max_length=20, default='', help_text='상장사')
    currency = models.CharField(max_length=10, blank=True, null=True, help_text='통화 단위')

    price = models.FloatField(default=0, help_text='주가')
    price_open = models.FloatField(default=0, help_text='시가')
    prevclose = models.FloatField(default=0, help_text='전일가')
    price_high = models.FloatField(default=0, help_text='고가')
    price_low = models.FloatField(default=0, help_text='저가')
    volume = models.FloatField(default=0, help_text='거래량')

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', auto_now_add=True)

    class Meta:
        ordering = ['ticker']

    def __str__(self): 
        return str(self.ticker)
    

class StockInformationHistory(models.Model): 
    """ 주식 실적 정보 히스토리
    pk = "id"
    columns = ["ticker", "update_date", "total_assets", "curruent_assets", "inventory", "quick_assets"
    , "non_current_assets", "investments", "tagible_assets", "liabilities", "current_liabilities", "non_current_liabilities"
    , "total_assets_ratio", "quick_assets_ratio", "liabilities_ratio", "total_revenue", "gross_profit", "operating_income"
    , "net_income", "total_revenue_ratio", "operating_income_ratio", "net_income_ratio", "operating_cash_flow"
    , "update_dt", "create_dt"]
    
    note: 종목마다 재무정보 항목에 차이가 있어, json filed로 변경해달라는 요청 있음
    """

    id = models.BigAutoField(help_text="id_stockinformationhistory", primary_key=True)
    ticker = models.ForeignKey("StockList", related_name="stockinformationhistory", on_delete=models.CASCADE, db_column = "ticker")
    update_date = models.DateField(verbose_name='date', help_text='업데이트 날짜', default=datetime.today)

    total_assets = models.FloatField(blank=True, null=True, help_text='자산총계')
    curruent_assets =  models.FloatField(blank=True, null=True, help_text='유동자산')
    inventory = models.FloatField(blank=True, null=True, help_text='재고자산')
    quick_assets = models.FloatField(blank=True, null=True, help_text='당좌자산')
    non_current_assets = models.FloatField(blank=True, null=True, help_text='비유동자산')
    investments = models.FloatField(blank=True, null=True, help_text='투자자산')
    tagible_assets = models.FloatField(blank=True, null=True, help_text='유형자산')
    liabilities = models.FloatField(blank=True, null=True, help_text='부채')
    current_liabilities = models.FloatField(blank=True, null=True, help_text='유동부채')
    non_current_liabilities = models.FloatField(blank=True, null=True, help_text='비유동부채')
    total_assets_ratio = models.FloatField(blank=True, null=True, help_text='유동비율')
    quick_assets_ratio = models.FloatField(blank=True, null=True, help_text='당좌비율')
    liabilities_ratio = models.FloatField(blank=True, null=True, help_text='부채비율')
    total_revenue = models.FloatField(blank=True, null=True, help_text='매출액')
    gross_profit = models.FloatField(blank=True, null=True, help_text='매출총이익')
    operating_income = models.FloatField(blank=True, null=True, help_text='영업이익')
    net_income = models.FloatField(blank=True, null=True, help_text='순이익')
    total_revenue_ratio = models.FloatField(blank=True, null=True, help_text='매출이익률')
    operating_income_ratio = models.FloatField(blank=True, null=True, help_text='영업이익률')
    net_income_ratio = models.FloatField(blank=True, null=True, help_text='순이익률')
    operating_cash_flow = models.FloatField(blank=True, null=True, help_text='영업현금흐름')

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', auto_now_add=True)

    class Meta:
        ordering = ['ticker','-update_date']

    def __str__(self): 
        return str(self.id)
    
    # def get_absolute_url(self):
    #     return reverse('stock_information_history-detail', args=(self.ticker))

class StockPriceHistory(models.Model): 
    """ 종목의 상장 이후 부터 현재까지 주가 히스토리, 히스토리 간격(interval): 1day
    pk = "id"
    columns = ["ticker", "update_date", "price_open", "price_high", "price_low", "price_close"
    , "adj_close", "volume", "splits", "dividends", "update_dt", "create_dt"]
    """

    id = models.BigAutoField(help_text="id_stockpricehistory", primary_key=True)
    ticker = models.ForeignKey("StockList", related_name="stockpricehistory", on_delete=models.CASCADE, db_column = "ticker")
    update_date = models.DateField(help_text='날짜', default=datetime.today)
    
    price_open = models.FloatField(blank=True, null=True, help_text="시가")
    price_high = models.FloatField(blank=True, null=True, help_text="고가")
    price_low = models.FloatField(blank=True, null=True, help_text="저가")
    price_close = models.FloatField(help_text="종가")
    volume = models.FloatField(blank=True, null=True, help_text="거래량")

    splits = models.FloatField(blank=True, null=True, help_text='주식분할 내역')
    dividends = models.FloatField(blank=True, null=True, help_text='배당 내역')

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', auto_now_add=True)

    class Meta:
        ordering = ['ticker', '-update_date' ]
    
    def __str__(self): 
        return str(self.ticker) + "@" + str(self.update_date)

    