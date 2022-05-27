import requests
import configparser


def get(API_KEY=None):
    # config API KEY
    if API_KEY is None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        API_KEY = config['CURRENCY_LAYER']['UserAPI']

    # making request 
    response  = requests.get(f"http://api.currencylayer.com/live?access_key={API_KEY}")
    return response.json().get("quotes", {})

if __name__ =="__main__":
    print(get())