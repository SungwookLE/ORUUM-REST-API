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

    #id = models.BigAutoField(help_text="id_stockinformationhistory", primary_key=True)
    ticker = models.OneToOneField("StockList", related_name="stockinformationhistory", on_delete=models.CASCADE, db_column = "ticker", primary_key=True)
    update_date = models.DateField(help_text='업데이트 날짜', default=datetime.today) # 

    
    yearly_income_statement = models.JSONField(help_text="연간 손익계산서", blank=True, null=True)
    yearly_balance_sheet= models.JSONField(help_text="연간 재무상태표", blank=True, null=True)
    yearly_cash_flow= models.JSONField(help_text="연간 현금흐름표", blank=True, null=True)

    quarterly_income_statement= models.JSONField(help_text="분기 손익계산서", blank=True, null=True)
    quarterly_balance_sheet= models.JSONField(help_text="분기 재무상태표", blank=True, null=True)
    quarterly_cash_flow= models.JSONField(help_text="분기 현금흐름표", blank=True, null=True)

    ttmPER = models.FloatField(help_text="trailing 12 months PER", blank=True, null=True)
    ttmPSR = models.FloatField(help_text="trailing 12 months PSR", blank=True, null=True)
    ttmPBR = models.FloatField(help_text="trailing 12 months PBR", blank=True, null=True)
    ttmPEGR = models.FloatField(help_text="trailing 12 months PEGR", blank=True, null=True)
    ttmEPS = models.FloatField(help_text="trailing 12 months EPS", blank=True, null=True)

    forwardPER = models.FloatField(help_text="forward PER", blank=True, null=True)
    forwardPSR = models.FloatField(help_text="forward PSR", blank=True, null=True)
    forwardEPS = models.FloatField(help_text="forward EPS", blank=True, null=True)

    marketCap = models.FloatField(help_text="marketCap", blank=True, null=True)

    fiftytwoweek_high = models.FloatField(help_text="52주 최고가", blank=True, null=True)
    fiftytwoweek_low  = models.FloatField(help_text="52주 최저가", blank=True, null=True)

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', auto_now_add=True)

    class Meta:
        ordering = ['ticker']

    def __str__(self): 
        return str(self.ticker)
    
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
    
class StockProfile(models.Model): 
    """ 종목의 상장 이후 부터 현재까지 주가 히스토리, 히스토리 간격(interval): 1day
    pk = "id"
    columns = ["ticker", "company_officers", "update_dt", "create_dt"]
    """

    # id = models.BigAutoField(help_text="id_stockprofile", primary_key=True)
    ticker = models.ForeignKey("StockList", related_name="stockprofile", on_delete=models.CASCADE, db_column = "ticker")
    update_date = models.DateField(help_text='날짜', default=datetime.today)
    
    company_officers = models.JSONField(help_text="회사 경영진", blank=True, null=True) 

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(verbose_name='create_dt', auto_now_add=True)

    class Meta:
        ordering = ['ticker', '-update_date' ]
    
    def __str__(self): 
        return str(self.ticker) + "@" + str(self.update_date)

    