from urllib.request import urlopen, Request
import pandas as pd
import numpy as np
import urllib

str_Url_fnguide_api_prefix = ["https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A",
                              "https://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A"]
str_Url_fnguide_api_postfix = ["&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701",
                               "&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701"]

class FnguideStockFinancialData():
    def get_Financial_raw_data(str_Ticker):
        str_Url_for_financial_data_from_fnguide = str_Url_fnguide_api_prefix[0] \
                                                + str_Ticker \
                                                + str_Url_fnguide_api_postfix[0]

        try:
            response_Stock_financial_data_request_to_fnguide = Request(str_Url_for_financial_data_from_fnguide, headers={'User-Agent': 'Mozilla/5.0'})
            html_Stock_finanacial_data_from_fnguide = urlopen(response_Stock_financial_data_request_to_fnguide).read()

            [dataframe_Annual_financial_data_from_fnguide,  dataframe_Quarter_financial_data_from_fnguide] = pd.read_html(html_Stock_finanacial_data_from_fnguide)

            dataframe_Annual_financial_data_from_fnguide.iloc[:,0] = dataframe_Annual_financial_data_from_fnguide.iloc[:,0].str.replace('계산에 참여한 계정 펼치기', '')  
            dataframe_Quarter_financial_data_from_fnguide.iloc[:,0] = dataframe_Quarter_financial_data_from_fnguide.iloc[:,0].str.replace('계산에 참여한 계정 펼치기', '')

            if "IFRS(연결)" in dataframe_Annual_financial_data_from_fnguide.columns:
                dataframe_Annual_financial_data_from_fnguide.set_index("IFRS(연결)", inplace=True) 

            elif "IFRS(별도)" in dataframe_Annual_financial_data_from_fnguide.columns:
                dataframe_Annual_financial_data_from_fnguide.set_index("IFRS(별도)", inplace=True) 
                
            if "IFRS(연결)" in dataframe_Quarter_financial_data_from_fnguide.columns:
                dataframe_Quarter_financial_data_from_fnguide.set_index("IFRS(연결)", inplace=True) 

            elif "IFRS(별도)" in dataframe_Quarter_financial_data_from_fnguide.columns:
                dataframe_Quarter_financial_data_from_fnguide.set_index("IFRS(별도)", inplace=True) 


        except (urllib.error.URLError, ValueError) as e:
            dataframe_Annual_financial_data_from_fnguide = None
            dataframe_Quarter_financial_data_from_fnguide = None

        str_Url_for_investment_indicators = str_Url_fnguide_api_prefix[1] \
                                          + str_Ticker \
                                          + str_Url_fnguide_api_postfix[1]

        try:
            response_Investment_indicators_from_API = Request(str_Url_for_investment_indicators, headers={'User-Agent': 'Mozilla/5.0'})
            html_Investment_indicators_from_fnguide = urlopen(response_Investment_indicators_from_API).read()

            dataframe_Annual_investment_indicators_from_fnguide = pd.read_html(html_Investment_indicators_from_fnguide)[1]
            dataframe_Annual_investment_indicators_from_fnguide.iloc[:,0] = dataframe_Annual_investment_indicators_from_fnguide.iloc[:,0].str.replace('계산에 참여한 계정 펼치기', '')   

            if "IFRS(연결)" in dataframe_Annual_investment_indicators_from_fnguide.columns:
                dataframe_Annual_investment_indicators_from_fnguide.set_index("IFRS(연결)", inplace=True) 

            elif "IFRS(별도)" in dataframe_Annual_investment_indicators_from_fnguide.columns:
                dataframe_Annual_investment_indicators_from_fnguide.set_index("IFRS(별도)", inplace=True) 

        except (urllib.error.URLError, ValueError) as e:
            dataframe_Annual_investment_indicators_from_fnguide = None

        dict_Financial_data_from_fnguide = {"Annual": dataframe_Annual_financial_data_from_fnguide,
                                            "Quarter": dataframe_Quarter_financial_data_from_fnguide,
                                            "Investment_indicator": dataframe_Annual_investment_indicators_from_fnguide}

        return dict_Financial_data_from_fnguide
    
    def process_Finance_raw_data(dict_Financial_data_from_fnguide):
        dataframe_Raw_annual_finance = dict_Financial_data_from_fnguide["Annual"]
        dataframe_Raw_annual_investment_indicator = dict_Financial_data_from_fnguide["Investment_indicator"]

        if dataframe_Raw_annual_finance is not None:
            if "ROA" in dataframe_Raw_annual_finance.index:
                dataframe_Raw_annual_finance = dataframe_Raw_annual_finance.loc[["ROA"]]
            else:
                dataframe_Raw_annual_finance.loc["ROA"] = np.nan
                dataframe_Raw_annual_finance = dataframe_Raw_annual_finance.loc[["ROA"]]

        if dataframe_Raw_annual_investment_indicator is not None:
            if "EV/EBITDA" in dataframe_Raw_annual_investment_indicator.index:
                dataframe_Raw_annual_investment_indicators = dataframe_Raw_annual_investment_indicator.loc[["EV/EBITDA"]]
            else:
                dataframe_Raw_annual_investment_indicator.loc["EV/EBITDA"] = np.nan
                dataframe_Raw_annual_investment_indicators = dataframe_Raw_annual_investment_indicator.loc[["EV/EBITDA"]]

        try:
            dataframe_Annual_finance = pd.concat([dataframe_Raw_annual_finance, dataframe_Raw_annual_investment_indicators])
            list_Annual_finanace_columns = dataframe_Annual_finance.columns
            list_New_columns = []
            for str_Column in list_Annual_finanace_columns:
                str_New_column = str_Column[:4] + "." + str_Column[5:]
                list_New_columns.append(str_New_column) 
            dataframe_Annual_finance.columns = list_New_columns
        except ValueError:
            dataframe_Annual_finance = None
        
        dict_Financial_data_from_fnguide = {"Annual": dataframe_Annual_finance}

        return dict_Financial_data_from_fnguide