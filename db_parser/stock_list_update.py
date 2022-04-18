# db_parser/stock_list_update.py
import json
from stocksymbol import StockSymbol  #https://medium.datadriveninvestor.com/download-list-of-all-stock-symbols-using-this-python-package-12937073b25
import numpy as np
import pandas as pd
import requests

class stock_list_db_update:
    def __init__(self):
        self.stocksymbol_api_key = '1d8591e0-fc08-43d6-96e4-d994844267b5'
        self.base_url = 'https://yfapi.net'
        self.yahoofinance_api_key ='Y6hHjQsoax7rghXMy9EDTwVIXRDhpJT7b5eHCvfg'
        self.stocksymbol_cursor = StockSymbol(self.stocksymbol_api_key)
        
    def get_symbol_list(self, nation, option=True):
        symbol_list = self.stocksymbol_cursor.get_symbol_list(market=nation, symbols_only=option) # "us" or "america" will also work
        return symbol_list

    def get_US_stock(self):
        stock_list = self.get_symbol_list("us")
        url = self.base_url+"/v6/finance/quote"
        headers = {'X-API-KEY':self.yahoofinance_api_key}

        symbol_str = ''
        for symbol in stock_list[0:50]:
            symbol_str += (str(symbol) +',')

        querystring = {'symbols': symbol_str }
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)

        for each in result["quoteResponse"]["result"]:
            for key in each.keys():
                if (key.find("Price")!=-1):
                    print(each["symbol"], each[key])

if __name__ =="__main__":
    test = stock_list_db_update()
    test.get_US_stock()





    