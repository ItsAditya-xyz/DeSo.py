import json
import requests


class Deso:
    def getDeSoPrice():  # returns deso price
        response = requests.get(
            "https://api.blockchain.com/v3/exchange/tickers/CLOUT-USD"
        )
        return response.json()
