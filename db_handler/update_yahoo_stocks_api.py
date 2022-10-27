#  file: db_handler/update_stocks_yahooapi.py
import FinanceDataReader as fdr
import os
import sys

import django
import requests

from tqdm import tqdm
import dbModule
import datetime
import re
from api.models import StockList, StockInformationHistory, StockPriceHistory


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.product")
django.setup()


class UpdateStocksFromYahooapi:
    """
    - 해당 클래스는 yahoo api https://yfapi.net 를 호출하여 데이터를 가져오고 db에 업데이트하는 코드
     - 장점: api를 이용하는 것이므로 리턴 값이 정형화 되어 있어, 핸들링하기 편함
     - 단점: API를 이용하기에 무료계정에서는, 호출 제한이 존재
    """

    def __init__(self, market):
        # self.database = dbModule.Database() # it is needed for handling database using raw SQL

        self.stockslisting_dict = self.get_symbollist_from_financedatareader(
            market)
        self.market = market

        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key = 'WSA8c7Ux102dDSwJAt8gq2STA5umMyuKTExXaoAc'

        '''
        yahoo api test key(for debug):
        self.yahoofinance_api_key = '5qYXdE6x0N768DcH5mdu76C7RlIjZI6I9wtltqbv' #@google 계정 api키
        self.yahoofinance_api_key = 'WSA8c7Ux102dDSwJAt8gq2STA5umMyuKTExXaoAc' #@naver 계정 api키
        self.yahoofinance_api_key = 'i5EPueJwqg2NEnHat9Xf82h9MI4JFiTF5pGKMy6W' #@daum 계정 api키
        '''

    def get_symbollist_from_financedatareader(self, market):
        '''
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
        symbollist_dict = fdr.StockListing(market)
        return symbollist_dict

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

    def update_stockquote_from_yahooapi(self):
        #현재 주식 가격
        url = self.base_url + "/v6/finance/quote"

        stockslisting_dict = self.stockslisting_dict.copy()
        progress_bar = tqdm(stockslisting_dict)
        progress_bar.set_description("stocklist from yFinance API")

        while (stockslisting_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 500
            stockslisting_dict_slice = stockslisting_dict.iloc[0:
                                                               maximum_number_of_stocks_loaded_at_once]

            query_symbols = ''
            if self.market in ["KOSPI", "KOSDAQ", "KRX", "KONEX"]:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+".KS,"
            else:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+","

            querystring = {"symbols": query_symbols}
            headers = {
                'x-api-key': self.yahoofinance_api_key
            }
            response_from_yahooapi = requests.request(
                "GET", url, headers=headers, params=querystring)

            stockslisting_dict.drop(
                stockslisting_dict_slice.index, inplace=True)
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
                                                 name_english=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "longName")[0:maximum_length_of_name],
                                                 name_korea=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "displayName")[0:maximum_length_of_name],
                                                 market=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "fullExchangeName"),
                                                 price=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketPrice", 'float'),
                                                 price_open=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketOpen", 'float'),
                                                 price_high=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketDayHigh", 'float'),
                                                 price_low=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketDayLow", 'float'),
                                                 prevclose=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketPreviousClose", 'float'),
                                                 volume=UpdateStocksFromYahooapi.get_value_from_dict(
                                                     yFinance_iter, "regularMarketVolume", 'float')
                                                 )

                    except KeyError as e:
                        print(f"response key:{e} is not existed. Continued...")

                    ################################################################################
                    # progress_bar가 100%가 되지 않는데,
                    # FinanceDataReader 패키지에서 제공하는 종목 중 일부가 yahooAPI에서 주가 정보를 제공하지 않는다.
                    # 즉, 두개의 database 간에 종목명의 정합성이 맞지 않아서 생기는 문제이다.
                    ################################################################################
                    progress_bar.update(1)

            except KeyError as e:
                print(
                    f"yFinance return is {self.result_json_from_yahooapi}. Maybe, Yahoo API Call Limited!!")
                return  # 일일 최대 호출 회수를 초과하면 request해도 response가 제대로 오지 않는다.

        return

    def update_stockpricehistory_from_yahooapi(self, history_range="1mo"):
        url = self.base_url + "/v8/finance/spark"

        stockslisting_dict = self.stockslisting_dict.copy()
        progress_bar = tqdm(stockslisting_dict)
        progress_bar.set_description("stockpricehistory from yFinance API")

        while (stockslisting_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 20
            stockslisting_dict_slice = stockslisting_dict.iloc[0:
                                                               maximum_number_of_stocks_loaded_at_once]

            query_symbols = ''
            if self.market == "KOSPI":
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+".KS,"
            elif self.market == "KOSDAQ":
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+".KQ,"
            else:
                for _, value in stockslisting_dict_slice.iterrows():
                    query_symbols += value["Symbol"]+","

            tick_interval = "1d"  # interval is 1-day
            querystring = {"symbols": query_symbols,
                           "range": history_range, "interval": tick_interval}
            headers = {'x-api-key': self.yahoofinance_api_key}
            response_from_yahooapi = requests.request(
                "GET", url, headers=headers, params=querystring)

            stockslisting_dict.drop(
                stockslisting_dict_slice.index, inplace=True)
            self.result_json_from_yahooapi = response_from_yahooapi.json()

            for result_iterator in self.result_json_from_yahooapi.values():
                try:
                    ticker = result_iterator["symbol"]
                except TypeError as e:
                    print(
                        f"yFinance return is {result_iterator}. Maybe, Yahoo API Call Limited!!")
                    return  # 일일 최대 호출 회수를 초과하면 request해도 response가 제대로 오지 않는다.
                try:
                    object_from_stocklist = StockList.objects.get(
                        ticker=ticker)
                    for price_close, timestamp in zip(self.result_json_from_yahooapi[ticker]['close'], self.result_json_from_yahooapi[ticker]['timestamp']):
                        update_date = datetime.datetime.utcfromtimestamp(
                            timestamp).strftime('%Y-%m-%d')
                        try:
                            object_from_stockpricehistory = StockPriceHistory.objects\
                                .filter(ticker=object_from_stocklist).get(update_date=update_date)

                            object_from_stockpricehistory.price_close = price_close
                            object_from_stockpricehistory.save()

                        except StockPriceHistory.DoesNotExist:
                            if price_close is not None:
                                StockPriceHistory.objects.create(
                                    ticker=object_from_stocklist, update_date=update_date, price_close=price_close)

                except StockList.DoesNotExist:
                    print(f"{ticker} 종목은 'api_stocklist'에 등록되지 않았네요. Continued...")

                progress_bar.update(1)

        return


if __name__ == "__main__":
    updater = UpdateStocksFromYahooapi("NASDAQ")
    updater.update_stockquote_from_yahooapi()
    updater.update_stockpricehistory_from_yahooapi(history_range="max")
