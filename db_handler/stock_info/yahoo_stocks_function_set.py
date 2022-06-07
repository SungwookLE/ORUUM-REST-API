
import yahoo_fin.stock_info as yf
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

    def build_url(ticker, start_date = None, end_date = None, interval = "1d"):
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
                "interval": interval}
        
        return site, params

    def get_history_data(ticker, start_date = None, end_date = None, index_as_date = True,
             interval = "1d", headers = {'User-Agent': 'Mozilla/5.0'}):
        '''Downloads historical stock price data into a pandas data frame.  Interval
        must be "1d", "1wk", "1mo", or "1m" for daily, weekly, monthly, or minute data.
        Intraday minute data is limited to 7 days.
        
        @param: ticker
        @param: start_date = None
        @param: end_date = None
        @param: index_as_date = True
        @param: interval = "1d"
        '''
        
        if interval not in ("1d", "1wk", "1mo", "1m"):
            raise AssertionError("interval must be of of '1d', '1wk', '1mo', or '1m'")
        
        # build and connect to URL
        site, params = YahooStockFunctionSet.build_url(ticker, start_date, end_date, interval)
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
        
            if interval != "1m":
                # if add in adjclose: frame["adjclose"] = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
                frame.index = pd.to_datetime(temp_time, unit="s")
                frame.index = frame.index.map(lambda dt: dt.floor("d"))
                frame = frame[["open", "high", "low",
                            "close", "volume"]]

            else:
                frame.index = pd.to_datetime(temp_time, unit="s")
                frame = frame[["open", "high", "low", "close", "volume"]]

            frame['ticker'] = ticker.upper()

            if not index_as_date:
                frame = frame.reset_index()
                frame.rename(columns={"index": "date"}, inplace=True)

        except KeyError as E:
            print(resp.url)
            print(f"{ticker} response has no column as {E}. Please Check!!\n")
            return None

        return frame

