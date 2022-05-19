#  file: db_handler/update_stocks_yahooapi.py

import FinanceDataReader as fdr
import os
import sys

import django
import requests  # for request API request

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
        self.database = dbModule.Database()
        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key = 'SWWKCLlCepeCqIA5qcICawFpEYJQeYz4YPMLmCk3'

        '''
        yahoo api test key(for debug):
        self.yahoofinance_api_key = 'B4MH0ErsUBavxjrK6p9bc3sKimfki0my2rvREKtd'  # @google 계정 api 키
        self.yahoofinance_api_key = 'SWWKCLlCepeCqIA5qcICawFpEYJQeYz4YPMLmCk3' #@naver 계정 api 키
        self.yahoofinance_api_key = 'e0mzom5Zj566VYXBngUMT2s91vsViidp8SXEuoJG' #@daum

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

    def get_symbol_list(self):
        return self.stocks_list["Symbol"]

    def get_dict_value(df, key, opt='str'):
        if opt != 'str':
            temp = (lambda x: 0 if x is None else x)(df.get(key))
        else:
            temp = (lambda x: "" if x is None else x)(df.get(key))

        if type(temp) == str:
            return re.sub(r"[^a-zA-Z0-9가-힣]", "", temp)
        else:
            return temp

    def update_stockquote_from_yahooapi(self, market):
        self.stocks_list = fdr.StockListing(market)
        url = self.base_url + "/v6/finance/quote"
        series = self.stocks_list[["Symbol", "Name"]]

        pbar = tqdm(series)
        pbar.set_description("yFinance API")

        while (series.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 500
            series_iter = series.iloc[0:maximum_number_of_stocks_loaded_at_once]

            query_symbols = ''
            if market == "KOSPI":
                for _, value in series_iter.iterrows():
                    query_symbols += value["Symbol"]+".KS,"
            else:
                for _, value in series_iter.iterrows():
                    query_symbols += value["Symbol"]+","

            querystring = {"symbols": query_symbols}
            headers = {
                'x-api-key': self.yahoofinance_api_key
            }
            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            series.drop(series_iter.index, inplace=True)
            self.patch_result = response.json()

            try:
                for yFinance_iter, fDataReader_iter in zip(self.patch_result["quoteResponse"]["result"], series_iter.iterrows()):
                    try:
                        obj = StockList.objects.get(
                            ticker=yFinance_iter["symbol"])
                        obj.update_date = datetime.date.today()

                        obj.price = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketPrice", 'float')

                        obj.price_open = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketOpen", 'float')

                        obj.price_high = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketDayHigh", 'float')

                        obj.price_low = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketDayLow", 'float')

                        obj.prevclose = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketPreviousClose", 'float')

                        obj.volume = UpdateStocksFromYahooapi.get_dict_value(
                            yFinance_iter, "regularMarketVolume", 'float')

                        obj.save()
                        pbar.update(1)

                    except StockList.DoesNotExist:
                        StockList.objects.create(ticker=yFinance_iter["symbol"], update_date=datetime.date.today(), name_english=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "longName")[0:50], name_korea=UpdateStocksFromYahooapi.get_dict_value(fDataReader_iter[1], "Name")[0:50], market=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "fullExchangeName"), price=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketPrice", 'float'), price_open=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketOpen", 'float'), price_high=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketDayHigh", 'float'), price_low=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketDayLow", 'float'), prevclose=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketPreviousClose", 'float'), volume=UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketVolume", 'float')
                                                 )
                        pbar.update(1)

                    except KeyError as e:
                        print(
                            "response key:{} is not existed.\ncontinued..".format(e))

            except KeyError as e:
                print(
                    "response에 key:{} is not existed.\nMaybe: Yahoo API Call Limit".format(e))
                break  # 일일 최대 호출 회수를 초과하면 request해도 response가 옳바르게 오지 않는다.

        return


if __name__ == "__main__":
    updater = UpdateStocksFromYahooapi()
    updater.update_stockquote_from_yahooapi("NASDAQ")
