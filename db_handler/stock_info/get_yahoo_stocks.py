import pandas as pd
from stock_info.get_tickers import GetTicker # 
from tqdm import tqdm
from stock_info.yahoo_stocks_function_set import YahooStockFunctionSet # stock_info.
import yahoo_fin.stock_info as yahoofin

"""
(6/10) 구현 필요한 함수: NOT YET IMPLEMENTED
get_dividends	(Ticker-Historical Data-Dividends Only) 배당일, 배당금
get_splits		(Ticker-Historical Data-Stock Split) 액면분할 날짜, 비율
"""


class YahooStockCrawler(GetTicker, YahooStockFunctionSet):
    def __init__(self, market):
        super().__init__(market)
        if self.market == "KOSPI":
            self.tickers_df["symbol"] = self.tickers_df["종목코드"].apply(
                lambda ticker: str(ticker).zfill(6) + ".KS")
        elif self.market == "KOSDAQ":
            self.tickers_df["symbol"] = self.tickers_df["종목코드"].apply(
                lambda ticker: str(ticker).zfill(6) + ".KQ")

    def get_tickers_df(self):
        return self.tickers_df

    def get_stocks_price(self):

        tickers_df = self.tickers_df.copy().sample(frac=1)
        stocks_price_df = pd.DataFrame()

        progress_bar = tqdm(tickers_df)
        progress_bar.set_description(f"{self.market}, stockprice-now")

        while (tickers_df.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 200
            ticker_df_slice = tickers_df.iloc[0:
                                              maximum_number_of_stocks_loaded_at_once]

            ticker_str = ""
            for ticker in ticker_df_slice["symbol"]:
                ticker_str += ticker+","

            tickers_df.drop(ticker_df_slice.index, inplace=True)

            result = pd.DataFrame(YahooStockCrawler.get_quote_data(ticker_str))
            stocks_price_df = pd.concat(
                [stocks_price_df, result], ignore_index=True, axis=0)

            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

        return stocks_price_df

    def get_stocks_price_history(self, range="max"):

        tickers_df = self.tickers_df.copy().sample(frac=1)
        stocks_price_history_df = pd.DataFrame()

        progress_bar = tqdm(tickers_df)
        progress_bar.set_description(f"{self.market}, stockprice-history")

        while (tickers_df.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 1
            ticker_df_slice = tickers_df.iloc[0:
                                              maximum_number_of_stocks_loaded_at_once]
            ticker_str = ""
            for ticker in ticker_df_slice["symbol"]:
                ticker_str += ticker

            tickers_df.drop(ticker_df_slice.index, inplace=True)
            result = YahooStockCrawler.get_history_data(
                ticker=ticker_str, range=range, index_as_date=False)

            stocks_price_history_df = pd.concat(
                [stocks_price_history_df, result], ignore_index=True, axis=0)
            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

        return stocks_price_history_df

    def get_stocks_information_history(self, yearly=True, quarterly=True):

        tickers_df = self.tickers_df.copy().sample(frac=1)

        progress_bar = tqdm(tickers_df)
        progress_bar.set_description(
            f"{self.market}, stockinformation-history")

        while (tickers_df.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 1
            ticker_df_slice = tickers_df.iloc[0:
                                              maximum_number_of_stocks_loaded_at_once]
            ticker_str = ""
            for ticker in ticker_df_slice["symbol"]:
                ticker_str += ticker

            tickers_df.drop(ticker_df_slice.index, inplace=True)
            dataframe_Raw_financial_data = YahooStockFunctionSet.get_financials(
                ticker=ticker_str, yearly=yearly, quarterly=quarterly)
            statistics_financial_data = YahooStockFunctionSet.get_statistics(
                ticker=ticker_str)

            # Yearly Data
            dataframe_yearly_income_statement_data = pd.concat(
                [(dataframe_Raw_financial_data["yearly_income_statement"])], axis=0)
            dataframe_yearly_balance_sheet_data = pd.concat(
                [(dataframe_Raw_financial_data["yearly_balance_sheet"])], axis=0)
            dataframe_yearly_cash_flow_data = pd.concat(
                [(dataframe_Raw_financial_data["yearly_cash_flow"])], axis=0)

            columns_yearly = dataframe_yearly_income_statement_data.columns.format()
            dataframe_yearly_income_statement_data.columns = columns_yearly
            dataframe_yearly_balance_sheet_data.columns = columns_yearly
            dataframe_yearly_cash_flow_data.columns = columns_yearly

            dataframe_yearly_income_statement_data.index.name = ticker_str
            dataframe_yearly_balance_sheet_data.index.name = ticker_str
            dataframe_yearly_cash_flow_data.index.name = ticker_str

            # Quarterly Data
            dataframe_quarterly_income_statement_data = pd.concat(
                [(dataframe_Raw_financial_data["quarterly_income_statement"])], axis=0)
            dataframe_quarterly_balance_sheet_data = pd.concat(
                [(dataframe_Raw_financial_data["quarterly_balance_sheet"])], axis=0)
            dataframe_quarterly_cash_flow_data = pd.concat(
                [(dataframe_Raw_financial_data["quarterly_cash_flow"])], axis=0)

            columns_quarterly = dataframe_quarterly_income_statement_data.columns.format()
            dataframe_quarterly_income_statement_data.columns = columns_quarterly
            dataframe_quarterly_balance_sheet_data.columns = columns_quarterly
            dataframe_quarterly_cash_flow_data.columns = columns_quarterly

            dataframe_quarterly_income_statement_data.index.name = ticker_str
            dataframe_quarterly_balance_sheet_data.index.name = ticker_str
            dataframe_quarterly_cash_flow_data.index.name = ticker_str

            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

            return_dataframe_list = [dataframe_yearly_income_statement_data, dataframe_yearly_balance_sheet_data, dataframe_yearly_cash_flow_data,
                                     dataframe_quarterly_income_statement_data, dataframe_quarterly_balance_sheet_data, dataframe_quarterly_cash_flow_data, statistics_financial_data]

            try:
                for dataframe in return_dataframe_list:
                    if dataframe.empty:
                        raise
                yield return_dataframe_list

            except:
                print(f"{ticker_str}: 리턴된 데이터프레임이 1개 이상 비어있어요.")
                yield [None]*len(return_dataframe_list)

    def get_stocks_profile(self):

        tickers_df = self.tickers_df.copy().sample(frac=1)

        progress_bar = tqdm(tickers_df)
        progress_bar.set_description(f"{self.market}, stock-profile")

        while (tickers_df.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 1
            ticker_df_slice = tickers_df.iloc[0:
                                                  maximum_number_of_stocks_loaded_at_once]
            ticker_str = ""
            for ticker in ticker_df_slice["symbol"]:
                ticker_str += ticker

            tickers_df.drop(ticker_df_slice.index, inplace=True)
            dataframe_profile_data = YahooStockFunctionSet.get_profile(ticker=ticker_str)

            return_dataframe_list = [dataframe_profile_data]

            progress_bar.update(1)
            
            try:
                for dataframe in return_dataframe_list:
                    if dataframe.empty:
                        raise
                yield return_dataframe_list

            except:
                print(f"{ticker_str}: 리턴된 데이터프레임이 1개 이상 비어있어요.") 
                yield [None]*len(return_dataframe_list)

if __name__ == "__main__":
    getter_stock = YahooStockCrawler("NASDAQ")
    # print(getter_stock.get_stocks_price()[["symbol","regularMarketPrice"]])
    # print(getter_stock.get_stocks_price_history())

    # for yearly_income_statement, yearly_balance_sheet, yearly_cash_flow, quarterly_income_statement, quarterly_balance_sheet, quarterly_cash_flow, statistics_financial_data in getter_stock.get_stocks_information_history():
    #     print(yearly_income_statement)
    #     print(yearly_balance_sheet)
    #     print(yearly_cash_flow)
    #     print(quarterly_income_statement)
    #     print(quarterly_balance_sheet)
    #     print(quarterly_cash_flow)
    #     print(statistics_financial_data)
    
    # print(getter_stock.get_stocks_profile())
    for profile_data in getter_stock.get_stocks_profile():
        print(profile_data)
