from dis import pretty_flags
import requests  # for request API request


class rec_my_api:
    def __init__(self):
        self.url = "http://localhost:8000/api"

    def get_datatime(self, ticker, s_date, e_date):
        url = self.url + "/stockinformation_spark/%s/%s-%s/"%(ticker, s_date, e_date)
        response = requests.request(
                "GET", url)

        
        print(response.json())

if __name__ == "__main__":
    parser = rec_my_api()
    parser.get_datatime("AAPL", "20220424", "20220426")