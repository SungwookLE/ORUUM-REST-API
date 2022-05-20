#  file: db_handler/get_stocks_oruum.py

import requests  

class GetStocksFromORUUM:
    def __init__(self):
        self.url = "http://localhost:8000/api"

    def get_spark(self, ticker, s_date, e_date):
        url = self.url + "/stockinformationspark/%s/%s-%s/"%(ticker, s_date, e_date)
        response = requests.request(
                "GET", url)
        return response.json()

if __name__ == "__main__":
    getter = GetStocksFromORUUM()
    response = getter.get_spark("AAPL", "20220424", "20220520")
    print(response)