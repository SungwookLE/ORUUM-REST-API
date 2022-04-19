# db_parser/stock_list_update.py
import json
import requests
import FinanceDataReader as fdr  # 종목명을 불러오기 위해 사용


class stock_list_db_update:
    def __init__(self):
        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key = 'Y6hHjQsoax7rghXMy9EDTwVIXRDhpJT7b5eHCvfg'
        self.stocks_list = fdr.StockListing('NASDAQ')  # 나스닥, 4608 종목
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

    def print_stock_list(self):
        print(self.stocks_list["Symbol"])

    def get_stock_price_from_yahooapi(self):
        url = self.base_url + "/v6/finance/quote"
        series = self.stocks_list["Symbol"]
        count = 0

        while (series.empty is not True):
            # yahoo finance  api에서 한번에 불러올 수 있는 종목 리스트의 개수 limit가 걸려있음
            series_iter = series.sample(n=30)

            query_symbols = ''
            for _, value in series_iter.items():
                query_symbols += value+","

            querystring = {"symbols": query_symbols}
            headers = {
                'x-api-key': self.yahoofinance_api_key
            }
            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            series.drop(series_iter.index)
            self.patch_result = response.json()

            try:
                for iter in self.patch_result["quoteResponse"]["result"]:
                    print(iter["symbol"], iter["regularMarketPrice"])
                    count += 1
            except KeyError as e:
                print("Err: json에 키{} 없음".format(e))
                break
            except:
                print("Err 발생")

            print("불러온 종목의 수:", count)

        return json.dumps(response.json(), indent=2)


if __name__ == "__main__":
    updater = stock_list_db_update()
    updater.get_stock_price_from_yahooapi()
