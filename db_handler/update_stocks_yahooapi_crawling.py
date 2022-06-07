#  file: db_handler/update_stocks_yahooapi.py

import FinanceDataReader as fdr
import os
import sys

import django
import numpy as np  
import math

from tqdm import tqdm
import dbModule
import datetime
import re

from stock_info.get_yahoo_stocks_price import YahooStockPrice

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.develop")
django.setup()
from api.models import StockList, StockInformationHistory, StockPriceHistory


class UpdateStocksFromYahooapi:
    def __init__(self, market):
        self.yf = YahooStockPrice(market)

        """
        getter_stock_price = YahooStockPrice("KOSDAQ")
        print(getter_stock_price.get_stocks_price()[["symbol","regularMarketPrice"]])
        print(getter_stock_price.get_stocks_price_history())
        """
    
    def get_value_from_dict(dataframe, key, value_type='str'):
        
        if value_type != 'str':
            # nan check를 위해 x!=x 인지 확인, nan인 경우 true 리턴
            value = (lambda x: 0 if x!=x else x)(dataframe.get(key))
        else:
            value = (lambda x: "" if x!=x else x)(dataframe.get(key))

        if type(value) == str:
            ret = re.sub(r"[^a-zA-Z0-9가-힣]", "", value)
        else:
            ret = value
        
        return ret

    def get_tickers_df(self):
        return self.yf.get_tickers_dict()

    def update_stockquote_from_yahooapi(self):

        #현재 주식 가격
        self.stocks_price_now = self.yf.get_stocks_price()
        for yFinance_idx, yFinance_value in self.stocks_price_now.iterrows():
            try:
                object_from_stocklist = StockList.objects.get(
                            ticker=yFinance_value["symbol"])
                object_from_stocklist.update_date = datetime.date.today()
                object_from_stocklist.price = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketPrice", 'float')
                object_from_stocklist.price_open = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketOpen", 'float')
                object_from_stocklist.price_high = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketDayHigh", 'float')
                object_from_stocklist.price_low = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketDayLow", 'float')
                object_from_stocklist.prevclose = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketPreviousClose", 'float')
                object_from_stocklist.volume = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_value, "regularMarketVolume", 'float')

                object_from_stocklist.save()

            except StockList.DoesNotExist:
                maximum_length_of_name = 50
                StockList.objects.create(ticker=yFinance_value["symbol"],
                                         update_date=datetime.date.today(), 
                                         name_english=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "longName")[0:maximum_length_of_name], 
                                         name_korea=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "displayName")[0:maximum_length_of_name], 
                                         market=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "fullExchangeName"), 
                                         price=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketPrice", 'float'), 
                                         price_open=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketOpen", 'float'), 
                                         price_high=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketDayHigh", 'float'), 
                                         price_low=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketDayLow", 'float'), 
                                         prevclose=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketPreviousClose", 'float'), 
                                         volume=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_value, "regularMarketVolume", 'float')
                                         )

        return

if __name__ == "__main__":
    updater = UpdateStocksFromYahooapi("NASDAQ")
    updater.update_stockquote_from_yahooapi()