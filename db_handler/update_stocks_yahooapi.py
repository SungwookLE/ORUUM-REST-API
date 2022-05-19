#  file: db_handler/update_stocks_yahooapi.py

import requests  # for request API request

from tqdm import tqdm
import dbModule
import datetime
import re
import pymysql
import json

# load stock list with symbol, name arond the market
import FinanceDataReader as fdr


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
        self.stocks_list = fdr.StockListing(market)  # 나스닥일 경우 4608종목
        url = self.base_url + "/v6/finance/quote"
        series = self.stocks_list[["Symbol", "Name"]]
        pbar = tqdm(series)
        pbar.set_description("yFinance API 종목 호출")

        while (series.empty is not True):
            # yahoo finance api에서 한번에 불러올 수 있는 종목 리스트의 개수 limit: 1000개 언저리인듯
            series_iter = series.iloc[0:500]

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
                        pbar.update(1)
                        sql = """
                        INSERT INTO
                        `api_stocklist` (`ticker`, `update_date`, `name_english`, `market`, `price`, `price_open`, `price_high`, `price_low`, `name_korea`, `prevclose`, `volume`, `update_dt`, `create_dt`) 
                        VALUES ('%s', '%s', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%f','%f', '%s', '%s');
                        """ % (yFinance_iter["symbol"], datetime.date.today(), UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "longName")[0:50],
                               UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "fullExchangeName"), UpdateStocksFromYahooapi.get_dict_value(
                                   yFinance_iter, "regularMarketPrice", 'float'),
                               UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketOpen", 'float'), UpdateStocksFromYahooapi.get_dict_value(
                                   yFinance_iter, "regularMarketDayHigh", 'float'),
                               UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketDayLow", 'float'), UpdateStocksFromYahooapi.get_dict_value(
                                   fDataReader_iter[1], "Name")[0:50],
                               UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketPreviousClose", 'float'), UpdateStocksFromYahooapi.get_dict_value(
                                   yFinance_iter, "regularMarketVolume", 'float'),
                               datetime.datetime.now(), datetime.datetime.now())

                        self.database.execute(sql)
                        self.database.commit()

                    except KeyError as e:
                        print(
                            "response key:{} is not existed.\n continued..".format(e))

                    except pymysql.err.IntegrityError as e:
                        #print(e.args[0])
                        # 중복된 pk 가 있어 db에 insert 하지 못하는 경우엔 update를 한다.
                        if (e.args[0] == 1062):
                            pbar.update(1)
                            sql = """
                            SELECT `update_dt` FROM `api_stocklist` WHERE `ticker`='%s' 
                            """ % yFinance_iter["symbol"]
                            rows = self.database.executeAll(sql)
                            timedelta = datetime.datetime.now() - \
                                rows[0]["update_dt"]

                            if (timedelta < datetime.timedelta(seconds=600)):
                                #print(timedelta) # 최종업데이트된 시간이 10분 이내라면, db업데이트 하지 않고 pass
                                pass
                            else:
                                sql = """
                                UPDATE `api_stocklist` SET `update_date` = '%s', `price`= '%f', 
                                    `price_open`= '%f', `price_high`= '%f', `price_low`= '%f', 
                                    `prevclose`= '%f', `volume`= '%f', `update_dt`= '%s'
                                WHERE `ticker`='%s'
                                """ % (datetime.date.today(), UpdateStocksFromYahooapi.get_dict_value(yFinance_iter, "regularMarketPrice", 'float'),
                                       UpdateStocksFromYahooapi.get_dict_value(
                                           yFinance_iter, "regularMarketOpen", 'float'),
                                       UpdateStocksFromYahooapi.get_dict_value(
                                           yFinance_iter, "regularMarketDayHigh", 'float'),
                                       UpdateStocksFromYahooapi.get_dict_value(
                                           yFinance_iter, "regularMarketDayLow", 'float'),
                                       UpdateStocksFromYahooapi.get_dict_value(
                                           yFinance_iter, "regularMarketPreviousClose", 'float'),
                                       UpdateStocksFromYahooapi.get_dict_value(
                                           yFinance_iter, "regularMarketVolume", 'float'),
                                       datetime.datetime.now(), yFinance_iter["symbol"])

                                self.database.execute(sql)
                                self.database.commit()

            except KeyError as e:
                print(
                    "response에 key:{} is not existed, so exit the program.\nCause: Yahoo API Call Limit".format(e))
                break  # 일일 최대 호출 회수를 초과하면 request해도 response가 옳바르게 오지 않는다.

        return


if __name__ == "__main__":
    updater = UpdateStocksFromYahooapi()
    updater.update_stockquote_from_yahooapi("NASDAQ")