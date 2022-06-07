from PyQt5.QtCore import QThread
from Backend.backend_stock_data.backend_stock_information import BackendStockInformation
import yfinance as yf
import datetime as date
import FinanceDataReader as fdr
import pandas as pd
import pandas_datareader.naver as nv
import time

class BackendStockPrice():
    def collect_Stock_price(str_Symbol,str_Market):
        dataframe_Stock_price = pd.DataFrame()
        datetime_Data_collection_start = date.datetime.now()
        int_Trial_number = 0
        while(dataframe_Stock_price.empty != False):
            bool_Time_passed_2seconds = date.datetime.now() > datetime_Data_collection_start+date.timedelta(seconds=2)
            bool_Time_passed_4seconds = date.datetime.now() > datetime_Data_collection_start+date.timedelta(seconds=4)

            bool_Market_us = str_Market == "NYSE" or str_Market == "NASDAQ"

            if (not bool_Time_passed_2seconds) and int_Trial_number == 0 and dataframe_Stock_price.empty == True:
                if(bool_Market_us):
                    print("[Backend] Finding....  using Yahoo Finance")
                    dataframe_Stock_price = yf.download(str_Symbol, date.datetime.today()-date.timedelta(365*5), date.datetime.today())
                    
                    if dataframe_Stock_price.empty == False:
                        print("[Backend] Collected Stock Price using Yahoo Finance")
                        return dataframe_Stock_price
                else:
                    print("[Backend] Finding....  using Naver Finance")
                    try:
                        dataframe_Stock_price = nv.NaverDailyReader(symbols=str_Symbol, start= date.datetime.today()-date.timedelta(365*5), end=date.datetime.today())
                        dataframe_Stock_price = dataframe_Stock_price.read()
                        dataframe_Stock_price = dataframe_Stock_price.astype(float)
                        dataframe_Stock_price['Adj Close'] = dataframe_Stock_price['Close']
                    except:
                        dataframe_Stock_price = pd.DataFrame()
                        pass
                    if dataframe_Stock_price.empty == False:
                        print("[Backend] Collected Stock Price using Naver Finance")
                        return dataframe_Stock_price
                
            elif (bool_Time_passed_2seconds and bool_Time_passed_4seconds) or int_Trial_number==1 and dataframe_Stock_price.empty == True:
                if(bool_Market_us):
                    print("[Backend] Finding....  using Finance Data Reader")
                    try:
                        dataframe_Stock_price = fdr.DataReader(str_Symbol, date.datetime.today()-date.timedelta(365*5), date.datetime.today())
                        dataframe_Stock_price['Adj Close'] = dataframe_Stock_price['Close']
                        dataframe_Stock_price.drop(columns=['Change'], inplace=True)
                    except:
                        int_Trial_number=2
                        pass
                    if dataframe_Stock_price.empty == False:
                        if not 'Volume' in dataframe_Stock_price.columns:
                            dataframe_Stock_price["Volume"] = 0
                            print("[Backend] Collect Stock Price using Finance Data Reader")
                        if not 'Open' in dataframe_Stock_price.columns:
                            dataframe_Stock_price["Open"] = dataframe_Stock_price["Close"]
                            print("[Backend] Collect Stock Price using Finance Data Reader")
                        if not 'High' in dataframe_Stock_price.columns:
                            dataframe_Stock_price["High"] = dataframe_Stock_price["Close"]
                            print("[Backend] Collect Stock Price using Finance Data Reader")
                        if not 'Low' in dataframe_Stock_price.columns:
                            dataframe_Stock_price["Low"] = dataframe_Stock_price["Close"]
                            print("[Backend] Collect Stock Price using Finance Data Reader")
                        if not 'Close' in dataframe_Stock_price.columns:
                            dataframe_Stock_price["Open"] = ""
                            dataframe_Stock_price["High"] = ""
                            dataframe_Stock_price["Low"] = ""
                            dataframe_Stock_price["Close"] = ""
                            dataframe_Stock_price["Adj Close"] = ""
                            dataframe_Stock_price["Volume"] = ""
                        return dataframe_Stock_price
                else:
                    print("[Backend] Finding....  using Yahoo Finance")
                    if str_Market == "KOSPI":
                        str_Symbol_kospi = str_Symbol + ".KS"
                        dataframe_Stock_price = yf.download(str_Symbol_kospi, date.datetime.today()-date.timedelta(365*5), date.datetime.today())
                    elif str_Market == "KOSDAQ":
                        str_Symbol_kosdaq = str_Symbol + ".KQ"
                        dataframe_Stock_price = yf.download(str_Symbol_kosdaq, date.datetime.today()-date.timedelta(365*5), date.datetime.today())
                    if dataframe_Stock_price.empty == False:
                        print("[Backend] Collected Stock Price using Yahoo Finance")
                        return dataframe_Stock_price
                    else:
                        int_Trial_number = 2
                        
            elif bool_Time_passed_4seconds or int_Trial_number==2:
                dataframe_Stock_price = pd.DataFrame()
                dataframe_Stock_price["Open"] = ""
                dataframe_Stock_price["High"] = ""
                dataframe_Stock_price["Low"] = ""
                dataframe_Stock_price["Close"] = ""
                dataframe_Stock_price["Adj Close"] = ""
                dataframe_Stock_price["Volume"] = ""
                return dataframe_Stock_price

class BackendStockPriceManager(QThread):
    def __init__(self,queue_bool_Request_stock_price_data,shared_str_Stock_price_data_request_ticker,queue_bool_Success_get_stock_price_data,
                 queue_Dataframe_stock_price_data,shared_str_Stock_company_name,shared_str_Stock_market,
                 queue_bool_Request_update_market_index,shared_str_Market_index_ticker,queue_bool_Success_get_market_index_price_data,queue_dataframe_Market_index_data,
                 queue_bool_Request_thread_finish):
        super().__init__()
        self.queue_bool_Request_stock_price_data = queue_bool_Request_stock_price_data
        self.shared_str_Stock_price_data_request_ticker = shared_str_Stock_price_data_request_ticker
        self.queue_bool_Success_get_stock_price_data = queue_bool_Success_get_stock_price_data
        self.queue_Dataframe_stock_price_data = queue_Dataframe_stock_price_data
        self.shared_str_Stock_company_name = shared_str_Stock_company_name
        self.shared_str_Stock_market = shared_str_Stock_market
        self.queue_bool_Request_update_market_index = queue_bool_Request_update_market_index
        self.shared_str_Market_index_ticker = shared_str_Market_index_ticker
        self.queue_bool_Success_get_market_index_price_data = queue_bool_Success_get_market_index_price_data
        self.queue_dataframe_Market_index_data = queue_dataframe_Market_index_data

        self.bool_Stock_information_colllect = False
        self.queue_bool_Request_thread_finish = queue_bool_Request_thread_finish
        self.bool_Working = True

    def run(self):
        while (self.bool_Working):
            if self.bool_Stock_information_colllect == False:
                self.dict_Stock_database = BackendStockInformation.load_Stock_information_database()                
                self.bool_Stock_information_colllect = True

            if not self.queue_bool_Request_stock_price_data.empty():
                bool_Stock_price_request = self.queue_bool_Request_stock_price_data.get()
                if bool_Stock_price_request == True:
                    try:
                        dataframe_Stock_information = BackendStockInformation.find_Stock_information(self.dict_Stock_database,self.shared_str_Stock_price_data_request_ticker.value)
                        if dataframe_Stock_information.empty == False:
                            dataframe_Stock_price = BackendStockPrice.collect_Stock_price(dataframe_Stock_information['symbol'].values[0],dataframe_Stock_information['market'].values[0])
                            self.shared_str_Stock_company_name.value = dataframe_Stock_information['name'].values[0]
                            self.shared_str_Stock_market.value = dataframe_Stock_information['market'].values[0]
                            self.queue_bool_Success_get_stock_price_data.put(True)
                            self.queue_Dataframe_stock_price_data.put(dataframe_Stock_price)
                        else:
                            self.queue_bool_Success_get_stock_price_data.put(False)
                            self.queue_Dataframe_stock_price_data.put(pd.DataFrame())
                    except:
                        self.queue_bool_Success_get_stock_price_data.put(False)
                        self.queue_Dataframe_stock_price_data.put(pd.DataFrame())
                        print("[Backend] failed to collect stock price")

            if not self.queue_bool_Request_update_market_index.empty():
                bool_Market_index_update_request = self.queue_bool_Request_update_market_index.get()
                if bool_Market_index_update_request == True:
                    try:
                        dataframe_Market_index = BackendStockPrice.collect_Stock_price(self.shared_str_Market_index_ticker.value,"NYSE")
                        self.queue_dataframe_Market_index_data.put(dataframe_Market_index)
                        self.queue_bool_Success_get_market_index_price_data.put(True)
                    except:
                        self.queue_bool_Success_get_market_index_price_data.put(False)
                        print("[Backend] failed to collect market index data")

            if not self.queue_bool_Request_thread_finish.empty():
                print("[Backend] stock price manager finished")
                self.bool_Working = False
                self.quit()
                self.wait()
            
            time.sleep(0.1)