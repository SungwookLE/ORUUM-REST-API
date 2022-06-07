from PyQt5.QtCore import QThread

import pandas as pd
import time

from Backend.backend_stock_data.backend_stock_information import BackendStockInformation
from Backend.backend_stock_data.naver_stock_finance import NaverStockFinancialData
from Backend.backend_stock_data.fnguide_stock_finance import FnguideStockFinancialData
from Backend.backend_stock_data.yahoo_finance_stock_finance import YahooFinanceFinancialData

list_Annual_financial_data_columns = ['-5y', '-4y', '-3y', '-2y', '-1y', "+1y(E)"]
list_Quarter_financial_data_columns = ['-5q', '-4q', '-3q', '-2q', '-1q', "+1q(E)"]

class BackendStockFinanceManager(QThread):
    def __init__(self,
                queue_bool_Request_stock_finance_data,
                shared_str_Stock_finance_data_request_ticker,
                queue_bool_Success_get_stock_finance_data,
                queue_dataframe_Stock_finance_data,
                queue_bool_Request_thread_finish):
        super().__init__()
        self.queue_bool_Request_stock_finance_data = queue_bool_Request_stock_finance_data
        self.shared_str_Stock_finance_data_request_ticker = shared_str_Stock_finance_data_request_ticker
        self.queue_bool_Success_get_stock_finance_data = queue_bool_Success_get_stock_finance_data
        self.queue_dataframe_Stock_finance_data = queue_dataframe_Stock_finance_data               

        self.queue_bool_Request_thread_finish = queue_bool_Request_thread_finish
        self.bool_Stock_information_colllect = False

        self.bool_Working = True

    def run(self):
        while (self.bool_Working):
            if self.bool_Stock_information_colllect == False:
                self.dict_Stock_database = BackendStockInformation.load_Stock_information_database()                
                self.bool_Stock_information_colllect = True

            if not self.queue_bool_Request_stock_finance_data.empty():
                bool_Stock_finance_request = self.queue_bool_Request_stock_finance_data.get()
                if bool_Stock_finance_request == True:                   
                    try:
                        dataframe_Stock_information = BackendStockInformation.find_Stock_information(self.dict_Stock_database, self.shared_str_Stock_finance_data_request_ticker.value)
                        self.shared_str_Stock_finance_data_request_ticker.value = dataframe_Stock_information['symbol'].values[0]
                        
                        dict_Financial_data = BackendStockFinance.get_Financial_data(dataframe_Stock_information['market'].values[0],
                                                                                     dataframe_Stock_information['symbol'].values[0])
                        self.queue_bool_Success_get_stock_finance_data.put(True)
                        self.queue_dataframe_Stock_finance_data.put(dict_Financial_data)
                    except:
                        self.queue_bool_Success_get_stock_finance_data.put(False)
                        print("[Backend] failed to collect stock finance")
                                    
            if not self.queue_bool_Request_thread_finish.empty():
                print("[Backend] stock finance data manager finished")
                self.bool_Working = False
                self.quit()
                self.wait()
            
            time.sleep(0.1)

class BackendStockFinance():
    def get_Financial_data(str_Market,str_Ticker):
        dataframe_Annual_financial_data = pd.DataFrame(columns=list_Annual_financial_data_columns)
        dataframe_Quarter_financial_data = pd.DataFrame(columns=list_Quarter_financial_data_columns)

        if str_Market == "NYSE" or str_Market == "NASDAQ":
            bool_Korean_market = False
        else:
            bool_Korean_market = True
        
        if bool_Korean_market == True:
            dict_Financial_data_from_naver = NaverStockFinancialData.get_Financial_raw_data(str_Ticker)
            dict_Financial_data_from_fnguide = FnguideStockFinancialData.get_Financial_raw_data(str_Ticker)

            dict_Financial_processed_data_from_naver = NaverStockFinancialData.process_Financial_raw_data(dict_Financial_data_from_naver)
            dict_Financial_processed_data_from_fnguide = FnguideStockFinancialData.process_Finance_raw_data(dict_Financial_data_from_fnguide)
            
            dataframe_Merged_annual_financial_data = BackendStockFinance.merge_Korean_annual_financial_data(dict_Financial_processed_data_from_naver,
                                                                                                     dict_Financial_processed_data_from_fnguide)
            dataframe_Merged_quarter_financial_data = BackendStockFinance.merge_Korean_quarter_financial_data(dict_Financial_processed_data_from_naver,
                                                                                                       dict_Financial_processed_data_from_fnguide)
            dataframe_Annual_financial_data = pd.concat([dataframe_Annual_financial_data, dataframe_Merged_annual_financial_data])
            dataframe_Quarter_financial_data = pd.concat([dataframe_Quarter_financial_data, dataframe_Merged_quarter_financial_data])

            dict_Financial_data = {"Current_finance" : dict_Financial_processed_data_from_naver["Current"], 
                                   "Annual_finance"  : dataframe_Annual_financial_data[list_Annual_financial_data_columns],
                                   "Quarter_finance" : dataframe_Quarter_financial_data[list_Quarter_financial_data_columns]}
        else:
            dict_Financial_data_from_yahoo_finance = YahooFinanceFinancialData.get_Financial_raw_data(str_Ticker)
            dict_Processed_financial_data_from_yahoo_finance = YahooFinanceFinancialData.process_Financial_raw_data(dict_Financial_data_from_yahoo_finance)

            dataframe_Annual_financial_data = pd.concat([dataframe_Annual_financial_data, dict_Processed_financial_data_from_yahoo_finance["Annual"]])
            dataframe_Quarter_financial_data = pd.concat([dataframe_Quarter_financial_data, dict_Processed_financial_data_from_yahoo_finance["Quarter"]])
            dataframe_Annual_and_quarter_financial_data = pd.concat([dataframe_Annual_financial_data, dataframe_Quarter_financial_data], axis = 1)

            dict_Financial_data = {"Current_finance" : dict_Processed_financial_data_from_yahoo_finance["Current"], 
                                   "Annual_finance" : dataframe_Annual_and_quarter_financial_data[list_Annual_financial_data_columns],
                                   "Quarter_finance" : dataframe_Annual_and_quarter_financial_data[list_Quarter_financial_data_columns]}
        return dict_Financial_data
    
    def merge_Korean_annual_financial_data(dict_Financial_processed_data_from_naver,dict_Financial_processed_data_from_fnguide):
        dataframe_Annual_financial_data_from_naver = dict_Financial_processed_data_from_naver["Annual"]
        dataframe_Annual_financial_data_from_fnguide = dict_Financial_processed_data_from_fnguide["Annual"]

        list_Target_dates = dataframe_Annual_financial_data_from_naver.columns
        
        if dataframe_Annual_financial_data_from_fnguide is None:
            dataframe_Annual_financial_data_from_fnguide = pd.DataFrame(columns=list_Target_dates, index=["ROA", "EV/EBITDA"])

        list_Source_dates = dataframe_Annual_financial_data_from_fnguide.columns
        list_Removal_dates = [date for date in list_Source_dates if date not in list_Target_dates]

        dataframe_Annual_financial_data_from_fnguide.drop(list_Removal_dates, axis=1, inplace=True)

        dataframe_Merged_annual_financial_data = pd.concat([dataframe_Annual_financial_data_from_naver, dataframe_Annual_financial_data_from_fnguide], axis=0)
        
        list_Merged_DB_dates = dataframe_Merged_annual_financial_data.columns
        liststr_Merged_DB_columns = list_Annual_financial_data_columns[-len(list_Merged_DB_dates):]

        dataframe_Merged_annual_financial_data.loc["날짜"] = list_Merged_DB_dates
        dataframe_Merged_annual_financial_data.columns = liststr_Merged_DB_columns

        return dataframe_Merged_annual_financial_data
    
    def merge_Korean_quarter_financial_data(dict_Financial_processed_data_from_naver, dict_Financial_processed_data_from_fnguide=None):
        dataframe_Quarter_financial_data_from_Naver = dict_Financial_processed_data_from_naver["Quarter"]
        list_Target_dates = dataframe_Quarter_financial_data_from_Naver.columns

        dataframe_Merged_quarter_financial_data = dataframe_Quarter_financial_data_from_Naver

        list_Merged_DB_dates = list_Target_dates
        list_Merged_DB_columns = list_Quarter_financial_data_columns[-len(list_Merged_DB_dates):]

        dataframe_Merged_quarter_financial_data.loc["날짜"] = list_Merged_DB_dates
        dataframe_Merged_quarter_financial_data.columns = list_Merged_DB_columns

        return dataframe_Merged_quarter_financial_data
    
    

    