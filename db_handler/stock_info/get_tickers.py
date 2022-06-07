import pandas as pd
import requests
#from bs4 import BeautifulSoup
#import yahoo_fin.stock_info as yf

class GetTicker:

    def __init__(self, market):
        self.korea_exchange = "https://kind.krx.co.kr/corpgeneral/corpList.do"
        self.usa_exchange = "https://api.nasdaq.com/api/screener/stocks"
        self.headers = {
            'User-Agent': 'Mozilla/5.0'}
        self.market = market
        self.tickers_dict = self.get_tickers()

    def get_tickers(self):

        if self.market == "NASDAQ" or self.market == "NYSE":
            if self.market == "NASDAQ":
                url = self.usa_exchange + \
                    f"?exchange={self.market}&download=true"
            elif self.market == "NYSE":
                url = self.usa_exchange + \
                    f"?exchange={self.market}&download=true"

            response = requests.get(url, headers=self.headers)
            result = pd.DataFrame(response.json()["data"]["rows"])

        elif self.market == "KOSPI" or self.market == "KOSDAQ":
            if self.market == "KOSPI":
                url = self.korea_exchange + f"?method=download&marketType=stockMkt"
            elif self.market == "KOSDAQ":
                url = self.korea_exchange + f"?method=download&marketType=kosdaqMkt"

            result = pd.read_html(url)[0]

        return result


if __name__ == "__main__":
    getter_NASDAQ_ticker = GetTicker("NASDAQ")
    NASDAQ_ticker_dict = getter_NASDAQ_ticker.get_tickers()

    getter_NYSE_ticker = GetTicker("NYSE")
    NYSE_ticker_dict = getter_NYSE_ticker.get_tickers()

    getter_KOSPI_ticker = GetTicker("KOSPI")
    KOSPI_ticker_dict = getter_KOSPI_ticker.get_tickers()

    getter_KOSDAQ_ticker = GetTicker("KOSDAQ")
    KOSDAQ_ticker_dict = getter_KOSDAQ_ticker.get_tickers()

    print(NASDAQ_ticker_dict)
    print(NYSE_ticker_dict)
    print(KOSPI_ticker_dict)
    print(KOSDAQ_ticker_dict)