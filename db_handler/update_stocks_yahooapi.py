#  file: db_handler/update_stocks_yahooapi.py

from turtle import up
import FinanceDataReader as fdr
import os
import sys

import django
import requests  

from tqdm import tqdm
import dbModule
import datetime
import re


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.develop")
django.setup()
from api.models import StockList, StockInformationHistory, StockPriceHistory


class UpdateStocksFromYahooapi:
    def __init__(self):
        self.database = dbModule.Database() # it is needed for handling database using raw SQL
        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key = '5qYXdE6x0N768DcH5mdu76C7RlIjZI6I9wtltqbv'

        '''
        yahoo api test key(for debug):
        self.yahoofinance_api_key = '5qYXdE6x0N768DcH5mdu76C7RlIjZI6I9wtltqbv' #@google 계정 api키
        self.yahoofinance_api_key = 'SWWKCLlCepeCqIA5qcICawFpEYJQeYz4YPMLmCk3' #@naver 계정 api키
        self.yahoofinance_api_key = 'e0mzom5Zj566VYXBngUMT2s91vsViidp8SXEuoJG' #@daum 계정 api키

        # KRX stock symbol list
        stocks = fdr.StockListing('KRX') # 코스피, 코스닥, 코넥스 전체
        stocks = fdr.StockListing('KOSPI') # 코스피
        stocks = fdr.StockListing('KOSDAQ') # 코스닥
        stocks = fdr.StockListing('KONEX') # 코넥스

        # NYSE, NASDAQ, AMEX stock symbol list
        stocks = fdr.StockListing('NYSE')   # 뉴욕거래소
        stocks= fdr.StockListing('NASDAQ') # 나스닥
        stocks = fdr.StockListing('AMEX')   # 아멕스
        '''

    def get_symbollist_from_financedatareader(self, market):
        symbollist_dict = fdr.StockListing(market)
        return symbollist_dict["Symbol"]

    def get_value_from_dict(dataframe, key, value_type='str'):
        if value_type != 'str':
            value = (lambda x: 0 if x is None else x)(dataframe.get(key))
        else:
            value = (lambda x: "" if x is None else x)(dataframe.get(key))

        if type(value) == str:
            ret = re.sub(r"[^a-zA-Z0-9가-힣]", "", value)
        else:
            ret = value

        return ret

    def update_stockquote_from_yahooapi(self, market):
        self.stockslisting_dict = fdr.StockListing(market)
        url = self.base_url + "/v6/finance/quote"

        progress_bar = tqdm(self.stockslisting_dict)
        progress_bar.set_description("stocklist from yFinance API")

        while (self.stockslisting_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 500
            stockslisting_dict_slice = self.stockslisting_dict.iloc[0:maximum_number_of_stocks_loaded_at_once]

            query_symbols = ''
            if market in ["KOSPI", "KOSDAQ", "KRX", "KONEX"]:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+".KS,"
            else:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+","

            querystring = {"symbols": query_symbols}
            headers = {
                'x-api-key': self.yahoofinance_api_key
            }
            response_from_yahooapi= requests.request(
                "GET", url, headers=headers, params=querystring)

            self.stockslisting_dict.drop(stockslisting_dict_slice.index, inplace=True)
            self.result_json_from_yahooapi = response_from_yahooapi.json()

            try:
                for yFinance_iter, fDataReader_iter in zip(self.result_json_from_yahooapi["quoteResponse"]["result"], stockslisting_dict_slice.iterrows()):
                    try:
                        object_from_stocklist = StockList.objects.get(
                            ticker=yFinance_iter["symbol"])
                        object_from_stocklist.update_date = datetime.date.today()
                        object_from_stocklist.price = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketPrice", 'float')
                        object_from_stocklist.price_open = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketOpen", 'float')
                        object_from_stocklist.price_high = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketDayHigh", 'float')
                        object_from_stocklist.price_low = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketDayLow", 'float')
                        object_from_stocklist.prevclose = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketPreviousClose", 'float')
                        object_from_stocklist.volume = UpdateStocksFromYahooapi.get_value_from_dict(
                            yFinance_iter, "regularMarketVolume", 'float')

                        object_from_stocklist.save()

                    except StockList.DoesNotExist:
                        maximum_length_of_name = 50
                        StockList.objects.create(ticker=yFinance_iter["symbol"],
                                                 update_date=datetime.date.today(), 
                                                 name_english=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "longName")[0:maximum_length_of_name], 
                                                 name_korea=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "displayName")[0:maximum_length_of_name], 
                                                 market=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "fullExchangeName"), 
                                                 price=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketPrice", 'float'), 
                                                 price_open=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketOpen", 'float'), 
                                                 price_high=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketDayHigh", 'float'), 
                                                 price_low=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketDayLow", 'float'), 
                                                 prevclose=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketPreviousClose", 'float'), 
                                                 volume=UpdateStocksFromYahooapi.get_value_from_dict(yFinance_iter, "regularMarketVolume", 'float')
                                                 )

                    except KeyError as e:
                        print(f"response key:{e} is not existed.\ncontinued..")
                    
                    ################################################################################
                    # progress_bar가 100%가 되지 않는데,
                    # FinanceDataReader 패키지에서 제공하는 종목 중 일부가 yahooAPI에서 주가 정보를 제공하지 않는다.
                    # 즉, 두개의 database 간에 종목명의 정합성이 맞지 않아서 생기는 문제이다.
                    ################################################################################
                    progress_bar.update(1)

            except KeyError as e:
                print(f"response에 key:{e} is not existed.\nMaybe, Yahoo API Call Limited")
                break  # 일일 최대 호출 회수를 초과하면 request해도 response가 옳바르게 오지 않는다.

        return

    def update_stockpricehistory_from_yahooapi(self, market, history_range="1mo"):
        self.stockslisting_dict = fdr.StockListing(market)
        url = self.base_url + "/v8/finance/spark"

        progress_bar = tqdm(self.stockslisting_dict)
        progress_bar.set_description("stockpricehistory from yFinance API")

        while (self.stockslisting_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 50
            stockslisting_dict_slice = self.stockslisting_dict.iloc[0:maximum_number_of_stocks_loaded_at_once]

            query_symbols = ''
            if market in ["KOSPI", "KOSDAQ", "KRX", "KONEX"]:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+".KS,"
            else:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+","

            tick_interval="1d" #1day
            querystring = {"symbols": query_symbols
                        ,"range": history_range
                        ,"interval": tick_interval}
            headers = {'x-api-key': self.yahoofinance_api_key}
            response_from_yahooapi= requests.request("GET", url, headers=headers, params=querystring)

            self.stockslisting_dict.drop(stockslisting_dict_slice.index, inplace=True)
            self.result_json_from_yahooapi = response_from_yahooapi.json()

            for ticker in stockslisting_dict_slice["Symbol"]:
                try:
                    object_from_stocklist = StockList.objects.get(ticker=ticker)
                    for price_close, timestamp in zip(self.result_json_from_yahooapi[ticker]['close'], self.result_json_from_yahooapi[ticker]['timestamp']):
                        update_date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
                        try:
                            object_from_stockpricehistory = StockPriceHistory.objects\
                            .filter(ticker=object_from_stocklist).get(update_date=update_date)

                            object_from_stockpricehistory.price_close = price_close
                            object_from_stockpricehistory.save()

                        except StockPriceHistory.DoesNotExist:
                            StockPriceHistory.objects.create(ticker = object_from_stocklist
                                                        ,update_date = update_date
                                                        ,price_close = price_close)

                except StockList.DoesNotExist:
                    print(f"stocklist에 등록되지 않은 {ticker} 종목입니다.\nstocklist에 먼저 추가해주세요.")
                
                progress_bar.update(1)

        return

if __name__ == "__main__":
    updater = UpdateStocksFromYahooapi()
    #updater.update_stockquote_from_yahooapi("NASDAQ")
    updater.update_stockpricehistory_from_yahooapi("NASDAQ", history_range="1wk")