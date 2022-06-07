import requests
import json
import pandas as pd

class BackendStockInformation():
    def load_Stock_information_database():
        dataframe_Kospi_database = BackendStockInformation.load_Stock_information_database_kospi()
        dataframe_Kosdaq_database = BackendStockInformation.load_Stock_information_database_kosdaq()
        dataframe_Nasdaq_database = BackendStockInformation.load_Stock_information_database_nasdaq()
        dataframe_Nyse_database = BackendStockInformation.load_Stock_information_database_nyse()

        dict_Stock_database = {"Kospi": dataframe_Kospi_database,
                               "Kosdaq": dataframe_Kosdaq_database,
                               "Nasdaq": dataframe_Nasdaq_database,
                               "Nyse": dataframe_Nyse_database}
        return dict_Stock_database

    def load_Stock_information_database_kospi():
        str_Database_ip = "http://39.127.38.122:5050"
        str_Url_check_stock_info = str_Database_ip +"/stock_info/send_stock_info"

        dict_Kospi_info = {
            "admin_id":"root",
            "admin_pw":"ubuntu",
            "market":"KOSPI"
        }

        response_Kospi_info = requests.post(str_Url_check_stock_info, 
                                            data=dict_Kospi_info)

        result_Kospi_info = json.loads(response_Kospi_info.json())
        dataframe_Kospi_database = pd.read_json(result_Kospi_info['STOCK_INFO'])
        return dataframe_Kospi_database
    
    def load_Stock_information_database_kosdaq():
        str_Database_ip = "http://39.127.38.122:5050"
        str_Url_check_stock_info = str_Database_ip +"/stock_info/send_stock_info"

        dict_Kosdaq_info = {
            "admin_id":"root",
            "admin_pw":"ubuntu",
            "market":"KOSDAQ"
        }

        response_Kosdaq_info = requests.post(str_Url_check_stock_info, 
                                            data=dict_Kosdaq_info)

        result_Kosdaq_info = json.loads(response_Kosdaq_info.json())
        dataframe_Kosdaq_database = pd.read_json(result_Kosdaq_info['STOCK_INFO'])
        return dataframe_Kosdaq_database

    def load_Stock_information_database_nasdaq():
        str_Database_ip = "http://39.127.38.122:5050"
        str_Url_check_stock_info = str_Database_ip +"/stock_info/send_stock_info"

        dict_Nasdaq_info = {
            "admin_id":"root",
            "admin_pw":"ubuntu",
            "market":"NASDAQ"
        }

        response_Nasdaq_info = requests.post(str_Url_check_stock_info, 
                                            data=dict_Nasdaq_info)

        result_Nasdaq_info = json.loads(response_Nasdaq_info.json())
        dataframe_Nasdaq_database = pd.read_json(result_Nasdaq_info['STOCK_INFO'])
        return dataframe_Nasdaq_database

    def load_Stock_information_database_nyse():
        str_Database_ip = "http://39.127.38.122:5050"
        str_Url_check_stock_info = str_Database_ip +"/stock_info/send_stock_info"

        dict_Nyse_info = {
            "admin_id":"root",
            "admin_pw":"ubuntu",
            "market":"NYSE"
        }

        response_Nyse_info = requests.post(str_Url_check_stock_info, 
                                            data=dict_Nyse_info)

        result_Nyse_info = json.loads(response_Nyse_info.json())
        dataframe_Nyse_database = pd.read_json(result_Nyse_info['STOCK_INFO'])
        return dataframe_Nyse_database

    def find_Stock_information(dict_Stock_database,str_Stock_find):
        dataframe_Stock_information = pd.DataFrame()
        for str_Market in dict_Stock_database.keys():
            dataframe_Stock_database = dict_Stock_database[str_Market]
            if (dataframe_Stock_database['symbol']==str_Stock_find).any():
                dataframe_Stock_information = dataframe_Stock_database[dataframe_Stock_database['symbol'].isin([str_Stock_find])]
            elif (dataframe_Stock_database['name']==str_Stock_find).any():
                dataframe_Stock_information = dataframe_Stock_database[dataframe_Stock_database['name'].isin([str_Stock_find])]
        return dataframe_Stock_information            
    

if __name__ == "__main__":
    import time
    time_Start = time.time()
    dict_Stock_database = BackendStockInformation.load_Stock_information_database()
    print(str(time.time() - time_Start))
    print(dict_Stock_database)
    time_Start = time.time()
    dataframe_Stock_information = BackendStockInformation.find_Stock_information(dict_Stock_database,"현대차")
    print(dataframe_Stock_information)
    print(str(time.time() - time_Start))
   