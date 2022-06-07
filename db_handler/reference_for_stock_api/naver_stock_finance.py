import pandas as pd
import numpy as np
import requests

str_Url_naver_api_prefix = "https://finance.naver.com/item/main.nhn?code="
str_Current_financial_data_columns = ["Current"]
str_Current_finance_data_index = ["시가총액", "상장주식수", "PER", "EPS", "PBR", "BPS","ROE", "추정PER", "추정EPS"]

class NaverStockFinancialData():
    def get_Financial_raw_data(str_Ticker):
        str_URL_for_financial_data_from_naver = str_Url_naver_api_prefix + str_Ticker
        response_Stock_financial_data_request_to_naver = requests.get(str_URL_for_financial_data_from_naver).text

        dataframe_Raw_html_from_naver = pd.read_html(response_Stock_financial_data_request_to_naver)
        dataframe_Raw_financial_data_from_naver = dataframe_Raw_html_from_naver[3]
        
        dataframe_Raw_financial_data_from_naver.set_index(('주요재무정보', '주요재무정보', '주요재무정보'), inplace=True)
        dataframe_Raw_financial_data_from_naver.index.rename('주요재무정보', inplace=True)
        dataframe_Raw_financial_data_from_naver.columns = dataframe_Raw_financial_data_from_naver.columns.droplevel(2)

        dataframe_Annual_financial_data_from_naver = pd.DataFrame(dataframe_Raw_financial_data_from_naver).xs('최근 연간 실적', axis=1) 
        dataframe_Quarter_financial_data_from_naver = pd.DataFrame(dataframe_Raw_financial_data_from_naver).xs('최근 분기 실적', axis=1)
        dataframe_Current_financial_data_from_naver = pd.concat([dataframe_Raw_html_from_naver[5], dataframe_Raw_html_from_naver[8]])

        del dataframe_Raw_html_from_naver

        dict_Financial_data_from_naver = {"Annual": dataframe_Annual_financial_data_from_naver,
                                          "Quarter": dataframe_Quarter_financial_data_from_naver,
                                          "Current": dataframe_Current_financial_data_from_naver}

        return dict_Financial_data_from_naver
    
    def process_Financial_raw_data(dict_Financial_data_from_naver):
        dataframe_Annual_financial_data = dict_Financial_data_from_naver["Annual"]
        dataframe_Processed_annual_financial_data = dataframe_Annual_financial_data.rename(index = {"ROE(지배주주)":"ROE",
                                                                                                    "EPS(원)":"EPS",
                                                                                                    "PER(배)":"PER:",
                                                                                                    "BPS(원)":"BPS",
                                                                                                    "PBR(배)":"PBR",
                                                                                                    "주당배당금(원)":"주당배당금",
                                                                                                    "시가배당률(%)":"시가배당률",
                                                                                                    "배당성향(%)":"배당성향"})
        dataframe_Processed_annual_financial_data.loc["매출액"] = NaverStockFinancialData.change_Financial_data_unit(dataframe_Processed_annual_financial_data.loc["매출액"])
        dataframe_Processed_annual_financial_data.loc["영업이익"] = NaverStockFinancialData.change_Financial_data_unit(dataframe_Processed_annual_financial_data.loc["영업이익"])

        dataframe_Quarter_financial_data = dict_Financial_data_from_naver["Quarter"]
        dataframe_Processed_quarter_financial_data = dataframe_Quarter_financial_data.rename(index = {"ROE(지배주주)":"ROE",
                                                                                                      "EPS(원)":"EPS",
                                                                                                      "PER(배)":"PER",
                                                                                                      "BPS(원)":"BPS",
                                                                                                      "PBR(배)":"PBR",
                                                                                                      "주당배당금(원)":"주당배당금",
                                                                                                      "시가배당률(%)":"시가배당률",
                                                                                                      "배당성향(%)":"배당성향"})
        dataframe_Processed_quarter_financial_data.loc["매출액"] = NaverStockFinancialData.change_Financial_data_unit(dataframe_Processed_quarter_financial_data.loc["매출액"])
        dataframe_Processed_quarter_financial_data.loc["영업이익"] = NaverStockFinancialData.change_Financial_data_unit(dataframe_Processed_quarter_financial_data.loc["영업이익"])

        dataframe_Processed_current_financial_data = pd.DataFrame(columns=str_Current_financial_data_columns, index=str_Current_finance_data_index)
        series_Current_finance_index = dict_Financial_data_from_naver["Current"][0]
        series_Current_finance_value = dict_Financial_data_from_naver["Current"][1]

        for str_Index, str_Value in zip(series_Current_finance_index, series_Current_finance_value):
            if str_Index == "시가총액":
                str_Value = str_Value.replace("억원","")
                str_Value = str_Value.replace(",","")
                if "조" in str_Value:
                    int_Market_cap = int(str_Value.split("조")[0])*100000000 + int(str_Value.split("조")[1])*10000
                else:
                    int_Market_cap = int(str_Value)*10000

                dataframe_Processed_current_financial_data.loc["시가총액", "Current"] = int_Market_cap

            elif str_Index == "상장주식수":
                dataframe_Processed_current_financial_data.loc["상장주식수", "Current"] = int(str_Value)

            elif str_Index == "추정PERlEPS":
                str_Estimated_per, str_Estimated_eps = str_Value.split("l")
                float_Estimated_per = NaverStockFinancialData.extract_Data(str_Estimated_per, "배", "float")
                float_Estimated_eps = NaverStockFinancialData.extract_Data(str_Estimated_eps, "원", "int")                
            
                dataframe_Processed_current_financial_data.loc["추정PER", "Current"] = float_Estimated_per
                dataframe_Processed_current_financial_data.loc["추정EPS", "Current"] = float_Estimated_eps

            elif str_Index[:7] == "PERlEPS":
                str_Per, str_Eps = str_Value.split("l")
                float_Per = NaverStockFinancialData.extract_Data(str_Per, "배", "float")
                float_Eps = NaverStockFinancialData.extract_Data(str_Eps, "원", "int")   

                dataframe_Processed_current_financial_data.loc["PER", "Current"] = float_Per
                dataframe_Processed_current_financial_data.loc["EPS", "Current"] = float_Eps

            elif str_Index[:7] == "PBRlBPS":
                str_Pbr, str_Bps = str_Value.split("l")
                float_Pbr = NaverStockFinancialData.extract_Data(str_Pbr, "배", "float")
                float_Bps = NaverStockFinancialData.extract_Data(str_Bps, "원", "int")   

                dataframe_Processed_current_financial_data.loc["PBR", "Current"] = float_Pbr
                dataframe_Processed_current_financial_data.loc["BPS", "Current"] = float_Bps
            else:
                pass
        dataframe_Processed_current_financial_data.loc["ROE", "Current"] = dataframe_Processed_annual_financial_data.loc["ROE"][-2]
        
        dict_Financial_data_from_naver = {"Annual": dataframe_Processed_annual_financial_data,
                                            "Quarter": dataframe_Processed_quarter_financial_data,
                                            "Current": dataframe_Processed_current_financial_data}
        return dict_Financial_data_from_naver
    
    def extract_Data(str_Source_data, str_Unit, str_Return_type="float"):
        list_Zipped_data = list((str_Source_data.replace(" ", "")).replace(",",""))
        try:
            int_Index_unit = list_Zipped_data.index(str_Unit)
                
            if str_Return_type == "float":
                void_Target_data = float("".join(list_Zipped_data[:int_Index_unit]))
            
            elif str_Return_type == "int":
                void_Target_data = int("".join(list_Zipped_data[:int_Index_unit]))

            else:
                void_Target_data = float("".join(list_Zipped_data[:int_Index_unit]))
            
            return void_Target_data

        except ValueError:
            return np.NaN
    
    def change_Financial_data_unit(series_Financial_data):
        for int_Data_index in range(len(series_Financial_data)):
            if series_Financial_data.iloc[int_Data_index] == "-":
                series_Financial_data.iloc[int_Data_index] = 0
            else:
                series_Financial_data.iloc[int_Data_index] = float(series_Financial_data.iloc[int_Data_index])*10000
        return series_Financial_data
    