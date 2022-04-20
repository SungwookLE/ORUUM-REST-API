
# file name : parser_stock_list.py
# pwd : /db_parser/parser_stock_list.py

import requests  # for request API request
# load stock list with symbol, name arond the market
import FinanceDataReader as fdr
from tqdm import tqdm
import dbModule  # db_parser/dbModule.py, For mysql database handling using pymysql package with sql language
import datetime  # time handling
import re  # regex
import pymysql
import json


class parser_stock_list:
    def __init__(self):
        self.database = dbModule.Database()
        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key = 'B4MH0ErsUBavxjrK6p9bc3sKimfki0my2rvREKtd'  # @google 계정 api 키
        # self.yahoofinance_api_key = 'Y6hHjQsoax7rghXMy9EDTwVIXRDhpJT7b5eHCvfg' #@naver 계정 api 키

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

    def symbol_list(self):
        return self.stocks_list["Symbol"]

    def update_stockquote_from_yahooapi(self, market):
        self.stocks_list = fdr.StockListing(market)  # 나스닥일 경우 4608종목
        url = self.base_url + "/v6/finance/quote"
        series = self.stocks_list[["Symbol", "Name"]]

        pbar = tqdm(series)
        pbar.set_description("yFinance API 종목 호출")

        while (series.empty is not True):
            # yahoo finance api에서 한번에 불러올 수 있는 종목 리스트의 개수 limit: 1000개 언저리인듯
            series_iter = series.iloc[0:1000]

            query_symbols = ''
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
                        pbar.update(1)
                        sql = """
                        INSERT INTO
                        `api_stock_list` (`ticker`, `update_day`, `name_english`, `market`, `price`, `price_open`, `price_high`, `price_low`, `name_korea`, `prevclose`, `volume`, `update_dt`, `create_dt`) 
                        VALUES ('%s', '%s', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%f','%f', '%s', '%s');
                        """ % (yFinance_iter["symbol"], datetime.date.today(), re.sub(r"[^a-zA-Z0-9]", "", yFinance_iter["longName"])[0:50],
                               yFinance_iter["fullExchangeName"], yFinance_iter["regularMarketPrice"], yFinance_iter[
                                   "regularMarketOpen"], yFinance_iter["regularMarketDayHigh"],
                               yFinance_iter["regularMarketDayLow"], re.sub(r"[^a-zA-Z0-9]", "", fDataReader_iter[1]["Name"])[0:50], yFinance_iter["regularMarketPreviousClose"], yFinance_iter["regularMarketVolume"], datetime.datetime.now(), datetime.datetime.now())

                        self.database.execute(sql)
                        self.database.commit()

                    except KeyError as e:
                        print(
                            "response key:{} is not existed.\n continued..".format(e))

                    except pymysql.err.IntegrityError as e:
                        print(e.args[0])
                        # 중복된 pk가 있어 db에 insert 하지 못하는 경우엔 update를 한다.
                        if (e.args[0] == 1062):
                            sql = """
                            SELECT `update_dt` FROM `api_stock_list` WHERE `ticker`='%s' 
                            """ % yFinance_iter["symbol"]
                            rows = self.database.executeAll(sql)
                            timedelta = datetime.datetime.now() - \
                                rows[0]["update_dt"]

                            if (timedelta < datetime.timedelta(seconds=600)):
                                #print(timedelta) # 최종업데이트된 시간이 10분 이내라면, db업데이트 하지 않고 pass
                                pass
                            else:
                                sql = """
                                UPDATE `api_stock_list` SET `update_day` = '%s', `price`= '%f', 
                                    `price_open`= '%f', `price_high`= '%f', `price_low`= '%f', 
                                    `prevclose`= '%f', `volume`= '%f', `update_dt`= '%s'
                                WHERE `ticker`='%s'
                                """ % (datetime.date.today(), yFinance_iter["regularMarketPrice"], yFinance_iter["regularMarketOpen"],
                                       yFinance_iter["regularMarketDayHigh"], yFinance_iter[
                                           "regularMarketDayLow"], yFinance_iter["regularMarketPreviousClose"],
                                       yFinance_iter["regularMarketVolume"], datetime.datetime.now(), yFinance_iter["symbol"])

                                self.database.execute(sql)
                                self.database.commit()

            except KeyError as e:
                print(
                    "response에 key:{} is not existed, so exit the program.\nCause: Yahoo API Call Limit".format(e))
                break  # 일일 최대 호출 회수를 초과하면 request해도 response가 옳바르게 오지 않는다.

        return


if __name__ == "__main__":
    parser = parser_stock_list()
    parser.update_stockquote_from_yahooapi("NASDAQ")
