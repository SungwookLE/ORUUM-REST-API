
import requests
import pandas as pd
from bs4 import BeautifulSoup

class YahooStockFunctionSet:

    def get_quote_data(ticker, headers={'User-Agent': 'Mozilla/5.0'}):
        site = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ticker
        resp = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
        if not resp.ok:
            raise AssertionError(
                f"Invalid response from server.  Check if ticker is valid.")
        json_result = resp.json()
        info = json_result["quoteResponse"]["result"]
        return info

    def build_url(ticker, start_date, end_date, range, interval):
        base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        if end_date is None:  
            end_seconds = int(pd.Timestamp("now").timestamp()) #1654527693
        else:
            end_seconds = int(pd.Timestamp(end_date).timestamp())
        if start_date is None:
            start_seconds = 7223400  # timestamp '7223400' is datetime.datetime(1970, 3, 25, 14, 30)
        else:
            start_seconds = int(pd.Timestamp(start_date).timestamp())
        
        site = base_url + ticker
        
        params = {"startDate": start_seconds, "endDate": end_seconds,
                "range": range, "interval": interval}
        
        return site, params

    def get_history_data(ticker, start_date = None, end_date = None, range = "max", interval="1d", index_as_date = True,
              headers = {'User-Agent': 'Mozilla/5.0'}):

        '''Downloads historical stock price data into a pandas data frame
        @param: ticker
        @param: start_date = None
        @param: end_date = None
        @param: index_as_date = True
        @param: range = max, 1d, 5d, 1mo, 3mo, 6mo, 17, ytd
        @param: interval = "1d", "1wk", "1mo", "1m"

        '''
        
        # build and connect to URL
        site, params = YahooStockFunctionSet.build_url(ticker=ticker, start_date=start_date, end_date=end_date, range=range, interval=interval)
        resp = requests.get(site, params = params, headers = headers)

        if not resp.ok:
            if resp.json()['chart']['error']['code'] == 'Not Found':
                print(f"{ticker} may be delisted. Skipped!")
                return None
            else:
                print (f"{ticker}", resp.json())
                return None
        
        # get JSON response
        data = resp.json()
        # get open / high / low / close data
        frame = pd.DataFrame(data["chart"]["result"]
                             [0]["indicators"]["quote"][0])

        try:
            # get the date info
            temp_time = data["chart"]["result"][0]["timestamp"]
            frame.index = pd.to_datetime(temp_time, unit="s")
            frame.index = frame.index.map(lambda dt: dt.floor("d"))
            frame = frame[["open", "high", "low",
                            "close", "volume"]]
            frame['ticker'] = ticker.upper()

            if not index_as_date:
                frame = frame.reset_index()
                frame.rename(columns={"index": "date"}, inplace=True)

        except KeyError as E:
            print(resp.url)
            print(f"{ticker} response has no column as {E}. Please Check!!\n")
            return None

        return frame

