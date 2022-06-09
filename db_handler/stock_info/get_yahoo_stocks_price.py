import pandas as pd
from stock_info.get_tickers import GetTicker
from tqdm import tqdm
from stock_info.yahoo_stocks_function_set import YahooStockFunctionSet

class YahooStockPrice(GetTicker, YahooStockFunctionSet):
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

            result = pd.DataFrame(YahooStockPrice.get_quote_data(ticker_str))
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
            result = YahooStockPrice.get_history_data(
                ticker_str, range=range, index_as_date=False)

            stocks_price_history_df = pd.concat(
                    [stocks_price_history_df, result], ignore_index=True, axis=0)
            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

        return stocks_price_history_df

if __name__ == "__main__":
    getter_stock_price = YahooStockPrice("NASDAQ")
    print(getter_stock_price.get_stocks_price()[["symbol","regularMarketPrice"]])
    print(getter_stock_price.get_stocks_price_history())