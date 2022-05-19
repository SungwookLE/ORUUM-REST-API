#  file: db_handler/get_stocks_oruum.py

from regex import D
import requests  

class GetStocksFromORUUM:
    def __init__(self):
        self.url = "http://localhost:8000/api"

    def get_datatime(self, ticker, s_date, e_date):
        url = self.url + "/stockinformationspark/%s/%s-%s/"%(ticker, s_date, e_date)
        response = requests.request(
                "GET", url)

        print(response.json())

if __name__ == "__main__":
    getter = GetStocksFromORUUM()
    getter.get_datatime("AAPL", "20220424", "20220426")