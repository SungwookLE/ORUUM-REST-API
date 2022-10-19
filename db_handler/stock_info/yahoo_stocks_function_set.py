
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import numpy as np


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
            end_seconds = int(pd.Timestamp("now").timestamp())  # 1654527693
        else:
            end_seconds = int(pd.Timestamp(end_date).timestamp())
        if start_date is None:
            # timestamp '7223400' is datetime.datetime(1970, 3, 25, 14, 30)
            start_seconds = 7223400
        else:
            start_seconds = int(pd.Timestamp(start_date).timestamp())

        site = base_url + ticker

        params = {"startDate": start_seconds, "endDate": end_seconds,
                  "range": range, "interval": interval}

        return site, params

    def get_history_data(ticker, start_date=None, end_date=None, range="max", interval="1d", index_as_date=True,
                         headers={'User-Agent': 'Mozilla/5.0'}):
        '''Downloads historical stock price data into a pandas data frame
        @param: ticker
        @param: start_date = None
        @param: end_date = None
        @param: index_as_date = True
        @param: range = max, 1d, 5d, 1mo, 3mo, 6mo, 17, ytd
        @param: interval = "1d", "1wk", "1mo", "1m"

        '''

        # build and connect to URL
        site, params = YahooStockFunctionSet.build_url(
            ticker=ticker, start_date=start_date, end_date=end_date, range=range, interval=interval)
        resp = requests.get(site, params=params, headers=headers)

        if not resp.ok:
            if resp.json()['chart']['error']['code'] == 'Not Found':
                print(f"{ticker} may be delisted. Skipped!")
                return None
            else:
                print(f"{ticker}", resp.json())
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

    def _parse_json(url, headers={'User-agent': 'Mozilla/5.0'}):
        html = requests.get(url=url, headers=headers).text

        json_str = html.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()

        try:
            data = json.loads(json_str)[
                'context']['dispatcher']['stores']['QuoteSummaryStore']
            #timeseries_data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteTimeSeriesStore']["timeSeries"]
        except:
            return '{}'
        else:
            # return data
            new_data = json.dumps(data).replace('{}', 'null')
            new_data = re.sub(
                r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

            json_info = json.loads(new_data)

            return json_info

    def _parse_table(json_info):

        df = pd.DataFrame(json_info)

        if df.empty:
            return df

        del df["maxAge"]

        df.set_index("endDate", inplace=True)
        df.index = pd.to_datetime(df.index, unit="s")

        df = df.transpose()
        df.index.name = "Breakdown"

        return df

    def get_financials(ticker, yearly=True, quarterly=True):
        '''Scrapes financials data from Yahoo Finance for an input ticker, including
        balance sheet, cash flow statement, and income statement.  Returns dictionary
        of results.
        
        @param: ticker
        @param: yearly = True
        @param: quarterly = True
        '''

        if not yearly and not quarterly:
            raise AssertionError("yearly or quarterly must be True")

        financials_site = "https://finance.yahoo.com/quote/" + ticker + \
            "/financials?p=" + ticker

        json_info = YahooStockFunctionSet._parse_json(financials_site)

        result = {}

        if yearly:
            temp = json_info["incomeStatementHistory"]["incomeStatementHistory"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["yearly_income_statement"] = table

            temp = json_info["balanceSheetHistory"]["balanceSheetStatements"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["yearly_balance_sheet"] = table

            temp = json_info["cashflowStatementHistory"]["cashflowStatements"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["yearly_cash_flow"] = table

        if quarterly:
            temp = json_info["incomeStatementHistoryQuarterly"]["incomeStatementHistory"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["quarterly_income_statement"] = table

            temp = json_info["balanceSheetHistoryQuarterly"]["balanceSheetStatements"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["quarterly_balance_sheet"] = table

            temp = json_info["cashflowStatementHistoryQuarterly"]["cashflowStatements"]
            table = YahooStockFunctionSet._parse_table(temp)
            result["quarterly_cash_flow"] = table

        return result

    def get_statistics(ticker):
        financials_site = "https://finance.yahoo.com/quote/" + ticker + \
            "/key-statistics?p=" + ticker

        json_info = YahooStockFunctionSet._parse_json(financials_site)

        df = pd.DataFrame(json_info)
        df.drop(['pageViews', 'financialsTemplate', 'price', 'quoteType',
                'calendarEvents', 'financialData', 'symbol'], axis=1, inplace=True)

        new_dict = dict()
        new_dict["ticker"] = ticker

        try:
            new_dict["ttmPER"] = df["summaryDetail"]["trailingPE"]
        except KeyError as E:
            new_dict["ttmPER"] = None
        try:
            new_dict["ttmPSR"] = df["summaryDetail"]["priceToSalesTrailing12Months"]
        except KeyError as E:
            new_dict["ttmPSR"] = None
        try:
            new_dict["ttmPBR"] = df["defaultKeyStatistics"]["priceToBook"]
        except KeyError as E:
            new_dict["ttmPBR"] = None
        try:
            new_dict["ttmPEGR"] = df["defaultKeyStatistics"]["pegRatio"]
        except KeyError as E:
            new_dict["ttmPEGR"] = None
        try:
            new_dict["forwardPER"] = df["defaultKeyStatistics"]["forwardPE"]
        except KeyError as E:
            new_dict["forwardPSR"] = None
        try:
            new_dict["marketCap"] = df["summaryDetail"]["marketCap"]
        except KeyError as E:
            new_dict["marketCap"] = None
        try:
            new_dict["forwardEPS"] = df["defaultKeyStatistics"]["forwardEps"]
        except KeyError as E:
            new_dict["forwardEPS"] = None
        try:
            new_dict["ttmEPS"] = df["defaultKeyStatistics"]["trailingEps"]
        except KeyError as E:
            new_dict["ttmEPS"] = None
        try:
            new_dict["fiftytwoweek_high"] = df["summaryDetail"]["fiftyTwoWeekHigh"]
        except KeyError as E:
            new_dict["fiftytwoweek_high"] = None

        try:
            new_dict["fiftytwoweek_low"] = df["summaryDetail"]["fiftyTwoWeekLow"]
        except KeyError as E:
            new_dict["fiftytwoweek_low"] = None

        # (10/12) yahoo finance에 forwardPSR 정보 없어 채울 수 없음..
        new_dict["forwardPSR"] = None

        new_df = pd.DataFrame(new_dict, index=['value']).transpose()
        new_df.replace({np.NaN: None}, inplace=True)

        return new_df
