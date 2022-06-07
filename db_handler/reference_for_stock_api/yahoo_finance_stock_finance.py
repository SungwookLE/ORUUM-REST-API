import yahoo_fin.stock_info as yf
import pandas as pd
import numpy as np

list_Annual_quarter_financial_data_index = ["매출액","영업이익","당기순이익","영업이익률","순이익률","ROE","부채비율","당좌비율","유보율","EPS",
                                            "PER","BPS", "PBR","주당배당금","시가배당률","배당성향","ROA","EV/EBITDA","날짜"]
list_Current_financial_data_index = ["시가총액","상장주식수","PER","EPS","PBR","BPS","추정PER","추정EPS","ROE","ROA","EV/EBITDA"]
list_Current_financial_data_columns = ["Current"]

class YahooFinanceFinancialData():
    def get_Financial_raw_data(str_Ticker):
        dataframe_Raw_current_financial_statistic_data = yf.get_stats(str_Ticker) 
        dataframe_Raw_current_valuation = yf.get_stats_valuation(str_Ticker) 
        dataframe_Raw_current_financial_summary = yf.get_quote_table(str_Ticker)
        dataframe_Raw_financial_data = yf.get_financials(str_Ticker) 

        dataframe_Raw_current_valuation.columns = ['Attribute', 'Value']
        dataframe_Raw_current_valuation.set_index(('Attribute'), inplace=True)
        dataframe_Raw_current_financial_statistic_data.set_index(('Attribute'), inplace=True)

        dataframe_Filtered_current_financial_statistic_data = dataframe_Raw_current_financial_statistic_data.loc[["Shares Outstanding 5", 
                                                                                                                    "Forward Annual Dividend Rate 4",
                                                                                                                    "Forward Annual Dividend Yield 4",
                                                                                                                    "Trailing Annual Dividend Rate 3",
                                                                                                                    "Trailing Annual Dividend Yield 3",
                                                                                                                    "Return on Assets (ttm)",
                                                                                                                    "Return on Equity (ttm)",
                                                                                                                    "Book Value Per Share (mrq)"]]

        dataframe_Filtered_annual_financial_data = pd.concat([(dataframe_Raw_financial_data["yearly_income_statement"]).loc[["totalRevenue", 
                                                                                                                                    "operatingIncome",
                                                                                                                                    "netIncome"]], 
                                                            (dataframe_Raw_financial_data["yearly_balance_sheet"]).loc[["totalLiab", 
                                                                                                                                    "totalStockholderEquity",
                                                                                                                                    "totalCurrentAssets",
                                                                                                                                    # "inventory",
                                                                                                                                    "totalCurrentLiabilities"]]], axis=0)
        
        dataframe_Filtered_quarter_financial_data = pd.concat([(dataframe_Raw_financial_data["quarterly_income_statement"]).loc[["totalRevenue", 
                                                                                                                                    "operatingIncome",
                                                                                                                                    "netIncome"]], 
                                                            (dataframe_Raw_financial_data["quarterly_balance_sheet"]).loc[["totalLiab", 
                                                                                                                                    "totalStockholderEquity",
                                                                                                                                    "totalCurrentAssets",
                                                                                                                                    # "inventory",
                                                                                                                                    "totalCurrentLiabilities"]]], axis=0)
        
        dict_Financial_data_from_yahoo_finance = {"Annual": dataframe_Filtered_annual_financial_data,
                                                  "Quarter": dataframe_Filtered_quarter_financial_data,
                                                  "Current_statistic": dataframe_Filtered_current_financial_statistic_data,
                                                  "Current_valuation": dataframe_Raw_current_valuation,
                                                  "Current_summary": dataframe_Raw_current_financial_summary}

        return dict_Financial_data_from_yahoo_finance
    
    def process_Financial_raw_data(dict_Financial_data_from_yahoo_finance):
        dataframe_Processed_annual_finance = YahooFinanceFinancialData.process_Annual_financial_data(dict_Financial_data_from_yahoo_finance)
        dataframe_Processed_quarter_finance = YahooFinanceFinancialData.process_Quarter_financial_data(dict_Financial_data_from_yahoo_finance)
        dataframe_Processed_current_finance = YahooFinanceFinancialData.process_Current_financial_data(dict_Financial_data_from_yahoo_finance)

        dict_Processed_financial_data_from_yahoo_finance = {"Annual": dataframe_Processed_annual_finance,
                                                            "Quarter": dataframe_Processed_quarter_finance,
                                                            "Current": dataframe_Processed_current_finance}
        return dict_Processed_financial_data_from_yahoo_finance
    
    def process_Annual_financial_data(dict_Financial_data_from_yahoo_finance):
        list_Financial_data_column_candidates = ["-1y", "-2y", "-3y", "-4y", "-5y"]
        
        dataframe_Raw_annual_financial_data = dict_Financial_data_from_yahoo_finance["Annual"]
        dataframe_Raw_current_statistic_data = dict_Financial_data_from_yahoo_finance["Current_statistic"]

        # Process Annual Finance
        list_Dates = dataframe_Raw_annual_financial_data.columns
        list_Date_in_regular_form = []

        for int_Idx in range(len(list_Dates)):
            list_Date_in_regular_form.append(str(list_Dates.year[int_Idx]) + "." + str(list_Dates.month[int_Idx]))
        
        list_Annual_financial_data_columns = list_Financial_data_column_candidates[:len(list_Dates)]
        dataframe_Raw_annual_financial_data.columns = list_Annual_financial_data_columns

        dataframe_Processed_annual_financial_data = pd.DataFrame(columns=list_Annual_financial_data_columns, index= list_Annual_quarter_financial_data_index)
        dataframe_Processed_annual_financial_data.loc["날짜", :] = list_Date_in_regular_form
        dataframe_Processed_annual_financial_data.loc["매출액", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_annual_financial_data.loc["totalRevenue", :])
        dataframe_Processed_annual_financial_data.loc["영업이익", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_annual_financial_data.loc["operatingIncome",:])
        dataframe_Processed_annual_financial_data.loc["당기순이익", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_annual_financial_data.loc["netIncome"])
        dataframe_Processed_annual_financial_data.loc["영업이익률", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Processed_annual_financial_data.loc["영업이익", :], dataframe_Processed_annual_financial_data.loc["매출액", :]) * 100.0
        dataframe_Processed_annual_financial_data.loc["순이익률", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Processed_annual_financial_data.loc["당기순이익", :], dataframe_Processed_annual_financial_data.loc["매출액", :]) * 100.0
        dataframe_Processed_annual_financial_data.loc["부채비율", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Raw_annual_financial_data.loc["totalLiab", :], dataframe_Raw_annual_financial_data.loc["totalStockholderEquity", :]) * 100.0
        # dataframe_Processed_annual_financial_data.loc["당좌비율", :] = (dataframe_Raw_annual_financial_data.loc["totalCurrentAssets", :] - dataframe_Raw_annual_financial_data.loc["inventory", :]) / dataframe_Raw_annual_financial_data.loc["totalCurrentLiabilities", :] * 100.0

        if (not (dataframe_Raw_current_statistic_data.loc["Trailing Annual Dividend Yield 3"].isna())[0] and
            not (dataframe_Raw_current_statistic_data.loc["Trailing Annual Dividend Rate 3"].isna())[0]):
            float_Annual_dividend_yield = YahooFinanceFinancialData.extract_Data(dataframe_Raw_current_statistic_data.loc["Trailing Annual Dividend Yield 3", "Value"], 
                                                                                 str_Return_type="float")
            float_Annual_dividend_rate = float(dataframe_Raw_current_statistic_data.loc["Trailing Annual Dividend Rate 3", "Value"])
            
            dataframe_Processed_annual_financial_data.loc["주당배당금", "-1y"] = float_Annual_dividend_rate
            dataframe_Processed_annual_financial_data.loc["시가배당률", "-1y"] = float_Annual_dividend_yield
        return dataframe_Processed_annual_financial_data
    
    def process_Quarter_financial_data(dict_Financial_data_from_yahoo_finance):
        list_Financial_data_column_candidates = ["-1q", "-2q", "-3q", "-4q", "-5q"]
        
        dataframe_Raw_quarter_financial_data = dict_Financial_data_from_yahoo_finance["Quarter"]
        dataframe_Raw_current_statistic_data = dict_Financial_data_from_yahoo_finance["Current_statistic"]

        # Process Annual Finance
        list_Dates = dataframe_Raw_quarter_financial_data.columns
        list_Date_in_regular_form = []

        for int_Idx in range(len(list_Dates)):
            list_Date_in_regular_form.append(str(list_Dates.year[int_Idx]) + "." + str(list_Dates.month[int_Idx]))
        
        list_Quarter_financial_data_columns = list_Financial_data_column_candidates[:len(list_Dates)]
        dataframe_Raw_quarter_financial_data.columns = list_Quarter_financial_data_columns
        dataframe_Processed_quarter_financial_data = pd.DataFrame(columns=list_Quarter_financial_data_columns, index= list_Annual_quarter_financial_data_index)
        
        dataframe_Processed_quarter_financial_data.loc["날짜", :] = list_Date_in_regular_form
        dataframe_Processed_quarter_financial_data.loc["매출액", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_quarter_financial_data.loc["totalRevenue", :])
        dataframe_Processed_quarter_financial_data.loc["영업이익", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_quarter_financial_data.loc["operatingIncome",:])
        dataframe_Processed_quarter_financial_data.loc["당기순이익", :] = YahooFinanceFinancialData.change_Financial_data_unit(dataframe_Raw_quarter_financial_data.loc["netIncome"])
        dataframe_Processed_quarter_financial_data.loc["영업이익률", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Processed_quarter_financial_data.loc["영업이익", :], dataframe_Processed_quarter_financial_data.loc["매출액", :]) * 100.0
        dataframe_Processed_quarter_financial_data.loc["순이익률", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Processed_quarter_financial_data.loc["당기순이익", :], dataframe_Processed_quarter_financial_data.loc["매출액", :]) * 100.0
        dataframe_Processed_quarter_financial_data.loc["부채비율", :] = YahooFinanceFinancialData.divide_Series_data(dataframe_Raw_quarter_financial_data.loc["totalLiab", :], dataframe_Raw_quarter_financial_data.loc["totalStockholderEquity", :]) * 100.0
        # dataframe_Processed_quarter_financial_data.loc["당좌비율", :] = (dataframe_Raw_quarter_financial_data.loc["totalCurrentAssets", :] - dataframe_Raw_quarter_financial_data.loc["inventory", :]) / dataframe_Raw_quarter_financial_data.loc["totalCurrentLiabilities", :] * 100.0

        return dataframe_Processed_quarter_financial_data
    
    def process_Current_financial_data(dict_Financial_data_from_yahoo_finance):
        dataframe_Raw_current_summary = dict_Financial_data_from_yahoo_finance["Current_summary"]
        dataframe_Raw_current_statistics = dict_Financial_data_from_yahoo_finance["Current_statistic"]
        dataframe_Raw_current_valuation = dict_Financial_data_from_yahoo_finance["Current_valuation"]

        dataframe_Current_financial_data = pd.DataFrame(columns=list_Current_financial_data_columns,index=list_Current_financial_data_index)

        # Get Data
        str_Market_cap = dataframe_Raw_current_summary["Market Cap"]
        str_Outstanding_shares = dataframe_Raw_current_statistics.loc["Shares Outstanding 5", "Value"]
        str_PER = dataframe_Raw_current_summary["PE Ratio (TTM)"]
        str_EPS = dataframe_Raw_current_summary["EPS (TTM)"]
        str_PBR = dataframe_Raw_current_valuation.loc["Price/Book (mrq)", "Value"]
        str_BPS = dataframe_Raw_current_statistics.loc["Book Value Per Share (mrq)", "Value"]
        str_Expected_PER = dataframe_Raw_current_valuation.loc["Forward P/E 1", "Value"]
        str_ROE = dataframe_Raw_current_statistics.loc["Return on Equity (ttm)", "Value"]
        str_ROA = dataframe_Raw_current_statistics.loc["Return on Assets (ttm)", "Value"]
        str_EVEBITDA = dataframe_Raw_current_valuation.loc["Enterprise Value/EBITDA 7", "Value"]

        # Data type casting
        int_Market_cap = YahooFinanceFinancialData.extract_Data(str_Market_cap, str_Return_type="int")/10000
        int_Outstanding_shares = YahooFinanceFinancialData.extract_Data(str_Outstanding_shares, str_Return_type="int")
        float_PER = float(str_PER)
        float_EPS = float(str_EPS)
        float_PBR = float(str_PBR)
        float_BPS = float(str_BPS)
        float_Expected_PER = float(str_Expected_PER)
        float_Expected_EPS = np.NaN
        try:
            float_ROE = YahooFinanceFinancialData.extract_Data(str_ROE, str_Return_type="float")
        except:
            float_ROE = np.NaN
        try:
            float_ROA = YahooFinanceFinancialData.extract_Data(str_ROA, str_Return_type="float")
        except:
            float_ROA = np.NaN
        float_EVEBITDA = float(str_EVEBITDA)

        dataframe_Current_financial_data.loc["시가총액", "Current"] = int_Market_cap
        dataframe_Current_financial_data.loc["상장주식수", "Current"] = int_Outstanding_shares
        dataframe_Current_financial_data.loc["PER", "Current"] = float_PER
        dataframe_Current_financial_data.loc["EPS", "Current"] = float_EPS
        dataframe_Current_financial_data.loc["PBR", "Current"] = float_PBR
        dataframe_Current_financial_data.loc["BPS", "Current"] = float_BPS
        dataframe_Current_financial_data.loc["추정PER", "Current"] = float_Expected_PER
        dataframe_Current_financial_data.loc["추정EPS", "Current"] = float_Expected_EPS
        dataframe_Current_financial_data.loc["ROE", "Current"] = float_ROE
        dataframe_Current_financial_data.loc["ROA", "Current"] = float_ROA
        dataframe_Current_financial_data.loc["EV/EBITDA", "Current"] = float_EVEBITDA

        return dataframe_Current_financial_data

    def extract_Data(str_Source_data, str_Return_type="int"):
        if "T" in str_Source_data:
            int_Index_unit = str_Source_data.index("T")
            void_Target_data = float(str_Source_data[:int_Index_unit])
            void_Target_data *= 1000000000000

        elif "B" in str_Source_data:
            int_Index_unit = str_Source_data.index("B")
            void_Target_data = float(str_Source_data[:int_Index_unit])
            void_Target_data *= 1000000000
            
        elif "M" in str_Source_data:
            int_Index_unit = str_Source_data.index("M")
            void_Target_data = float(str_Source_data[:int_Index_unit])
            void_Target_data *= 1000000
            
        elif "%" in str_Source_data:
            int_Index_unit = str_Source_data.index("%")
            void_Target_data = float(str_Source_data[:int_Index_unit])     
        
        else:
            void_Target_data = float(str_Source_data)

        if str_Return_type == "int":
            return int(void_Target_data)
        
        elif str_Return_type == "float":
            return float(void_Target_data)
        
        else:
            return void_Target_data
        
    def change_Financial_data_unit(series_Financial_data):
        for int_Data_index in range(len(series_Financial_data)):
            series_Financial_data.iloc[int_Data_index] = float(series_Financial_data.iloc[int_Data_index])/10000
        return series_Financial_data
    
    def divide_Series_data(series_Data_son,series_Data_mother):
        series_Data_result = series_Data_son.copy()
        for int_Data_index in range(len(series_Data_son)):
            if series_Data_mother.iloc[int_Data_index] != 0:
                series_Data_result.iloc[int_Data_index] = series_Data_son.iloc[int_Data_index]/series_Data_mother.iloc[int_Data_index]
            else:
                series_Data_result.iloc[int_Data_index] = 0
        return series_Data_result