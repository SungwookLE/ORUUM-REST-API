#  file: db_handler/update_stocks_yahooapi.py
from locale import currency
import os
import sys
from tqdm import tqdm

import django

import datetime
import re

from stock_info.get_yahoo_stocks import YahooStockCrawler

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.develop")
django.setup()
from api.models import StockList, StockInformationHistory, StockPriceHistory


class UpdateStocksFromYahoo:
    """
    - 해당 클래스는 yahoo finance 사이트를 크롤링하여 데이터를 가져오고 db에 업데이트하는 코드
     - 장점: API를 이용하는 것이 아니므로, 호출 제한은 없다.
     - 단점: 리턴 값이 정형화되어 있지 않아, 데이터를 확인하면서 코드를 작성해야 함
    """

    def __init__(self, market):
        self.yf = YahooStockCrawler(market)

    def get_value_from_dict(dataframe, key, value_type):
        if value_type == 'str':
            # nan check를 위해 x!=x 의 조건문 사용하여, nan인 경우 true 리턴
            value = (lambda x: "" if x!=x else x)(dataframe.get(key))
            ret = re.sub(r"[^a-zA-Z0-9가-힣]", "", value)
        else:
            value = (lambda x: 0 if x!=x else x)(dataframe.get(key))
            ret = value
        return ret

    def get_tickers_df(self):
        return self.yf.get_tickers_df()

    def update_stockquote_from_yahoo(self):
        #현재 주식 가격
        self.stocks_price_now = self.yf.get_stocks_price()

        progress_bar = tqdm(self.stocks_price_now)
        progress_bar.set_description("StockList Database Update")

        for yFinance_idx, yFinance_value in self.stocks_price_now.iterrows():
            try:
                object_from_stocklist = StockList.objects.get(
                            ticker=yFinance_value["symbol"])
                object_from_stocklist.update_date = datetime.date.today()
                object_from_stocklist.price = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketPrice", 'float')
                object_from_stocklist.price_open = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketOpen", 'float')
                object_from_stocklist.price_high = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketDayHigh", 'float')
                object_from_stocklist.price_low = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketDayLow", 'float')
                object_from_stocklist.prevclose = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketPreviousClose", 'float')
                object_from_stocklist.volume = UpdateStocksFromYahoo.get_value_from_dict(
                            yFinance_value, "regularMarketVolume", 'float')

                object_from_stocklist.save()

            except StockList.DoesNotExist:
                maximum_length_of_name = 50
                StockList.objects.create(ticker=yFinance_value["symbol"],
                                         update_date=datetime.date.today(), 
                                         name_english=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "displayName", 'str')[0:maximum_length_of_name],
                                         name_korea=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "longName", 'str')[0:maximum_length_of_name],
                                         market=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "fullExchangeName", 'str'), 
                                         price=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketPrice", 'float'), 
                                         price_open=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketOpen", 'float'), 
                                         price_high=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketDayHigh", 'float'), 
                                         price_low=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketDayLow", 'float'), 
                                         prevclose=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketPreviousClose", 'float'), 
                                         volume=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "regularMarketVolume", 'float'),
                                         currency=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "currency", 'str')
                                         )
            
            progress_bar.update(1)

        return

    def update_stocks_price_history_from_yahoo(self, range="max"):
        #주식 가격 히스토리
        self.stocks_price_history = self.yf.get_stocks_price_history(range=range)

        progress_bar = tqdm(self.stocks_price_history)
        progress_bar.set_description("StockPriceHistory Database Update")

        for yFinance_idx, yFinance_value in self.stocks_price_history.iterrows():
            object_from_stocklist = StockList.objects.get(ticker=yFinance_value["ticker"])
            try:
                object_from_stockpricehistory = StockPriceHistory.objects.filter(
                            ticker=object_from_stocklist).get(update_date=yFinance_value["date"])

            except StockPriceHistory.DoesNotExist:
                StockPriceHistory.objects.create(ticker=object_from_stocklist,
                                         update_date=yFinance_value["date"], 
                                         price_open=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "open", 'float'),
                                         price_high=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "high", 'float'),
                                         price_low=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "low", 'float'), 
                                         price_close=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "close", 'float'), 
                                         volume=UpdateStocksFromYahoo.get_value_from_dict(yFinance_value, "volume", 'float'), 
                                         )
            
            progress_bar.update(1)

        return

    def update_stocks_information_history_from_yahoo(self):
        
        for yearly_income_statement, yearly_balance_sheet, yearly_cash_flow, quarterly_income_statement, quarterly_balance_sheet, quarterly_cash_flow in self.yf.get_stocks_information_history():
            
            try:
                json_yearly_income_statement_data = yearly_income_statement.to_json(orient = 'columns')
                json_yearly_balance_sheet_data = yearly_balance_sheet.to_json(orient = 'columns')
                json_yearly_cash_flow_data = yearly_cash_flow.to_json(orient = 'columns')
                
                json_quarterly_income_statement_data = quarterly_income_statement.to_json(orient = 'columns')
                json_quarterly_balance_sheet_data = quarterly_balance_sheet.to_json(orient = 'columns')
                json_quarterly_cash_flow_data = quarterly_cash_flow.to_json(orient = 'columns')
                ticker = yearly_income_statement.index.name

                object_from_stocklist = StockList.objects.get(ticker=ticker)
            
            except:
                print("pass...")

            else:
                try:
                    object_from_stockinformationhistory = StockInformationHistory.objects.get(
                                ticker=object_from_stocklist)
                    object_from_stockinformationhistory.yearly_income_statement = json_yearly_income_statement_data
                    object_from_stockinformationhistory.yearly_balance_sheet = json_yearly_balance_sheet_data
                    object_from_stockinformationhistory.yearly_cash_flow = json_yearly_cash_flow_data
                    object_from_stockinformationhistory.quarterly_income_statement = json_quarterly_income_statement_data
                    object_from_stockinformationhistory.quarterly_balance_sheet = json_quarterly_balance_sheet_data
                    object_from_stockinformationhistory.quarterly_cash_flow = json_quarterly_cash_flow_data


                except StockInformationHistory.DoesNotExist:
                    StockInformationHistory.objects.create(ticker=object_from_stocklist,
                                            yearly_income_statement=json_yearly_income_statement_data,
                                            yearly_balance_sheet=json_yearly_balance_sheet_data,
                                            yearly_cash_flow=json_yearly_cash_flow_data, 
                                            quarterly_income_statement=json_quarterly_income_statement_data, 
                                            quarterly_balance_sheet=json_quarterly_balance_sheet_data, 
                                            quarterly_cash_flow=json_quarterly_cash_flow_data
                                            )

if __name__ == "__main__":
    updater = UpdateStocksFromYahoo("NASDAQ")
    updater.update_stockquote_from_yahoo()
    updater.update_stocks_price_history_from_yahoo(range="max")
    updater.update_stocks_information_history_from_yahoo()