import pandas as pd
from stock_info.get_tickers import GetTicker
from tqdm import tqdm
from stock_info.yahoo_stocks_function_set import YahooStockFunctionSet

class YahooStockPrice(GetTicker, YahooStockFunctionSet):

    def __init__(self, market):
        super().__init__(market)
        if self.market == "KOSPI":
            self.tickers_dict["symbol"] = self.tickers_dict["종목코드"].apply(
                lambda ticker: str(ticker).zfill(6) + ".KS")
        elif self.market == "KOSDAQ":
            self.tickers_dict["symbol"] = self.tickers_dict["종목코드"].apply(
                lambda ticker: str(ticker).zfill(6) + ".KQ")

    def get_tickers_dict(self):
        return self.tickers_dict

    def get_stocks_price(self):

        tickers_dict = self.tickers_dict.copy().sample(frac=1)
        stocks_price_dict = pd.DataFrame()

        progress_bar = tqdm(tickers_dict)
        progress_bar.set_description(f"{self.market}, stockprice-now")

        while (tickers_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 200
            ticker_dict_slice = tickers_dict.iloc[0:
                                                  maximum_number_of_stocks_loaded_at_once]

            ticker_str = ""
            for ticker in ticker_dict_slice["symbol"]:
                ticker_str += ticker+","

            tickers_dict.drop(ticker_dict_slice.index, inplace=True)

            result = pd.DataFrame(YahooStockPrice.get_quote_data(ticker_str))
            stocks_price_dict = pd.concat(
                [stocks_price_dict, result], ignore_index=True, axis=0)

            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

        return stocks_price_dict

    def get_stocks_price_history(self):

        tickers_dict = self.tickers_dict.copy().sample(frac=1)
        stocks_price_history_dict = pd.DataFrame()

        progress_bar = tqdm(tickers_dict)
        progress_bar.set_description(f"{self.market}, stockprice-history")

        while (tickers_dict.empty is not True):
            maximum_number_of_stocks_loaded_at_once = 1
            ticker_dict_slice = tickers_dict.iloc[0:
                                                  maximum_number_of_stocks_loaded_at_once]
            ticker_str = ""
            for ticker in ticker_dict_slice["symbol"]:
                ticker_str += ticker

            tickers_dict.drop(ticker_dict_slice.index, inplace=True)
            result = YahooStockPrice.get_history_data(
                ticker_str, index_as_date=False)

            stocks_price_history_dict = pd.concat(
                    [stocks_price_history_dict, result], ignore_index=True, axis=0)
                
            progress_bar.update(maximum_number_of_stocks_loaded_at_once)

        return stocks_price_history_dict

if __name__ == "__main__":
    getter_stock_price = YahooStockPrice("KOSDAQ")
    print(getter_stock_price.get_stocks_price()[["symbol","regularMarketPrice"]])
    print(getter_stock_price.get_stocks_price_history())