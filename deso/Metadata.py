from deso.utils import getUserJWT
import requests


class Metadata:
    def __init__(self, publicKey="BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg", nodeURL="https://node.deso.org/api/v0/"):
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL

    def getNodeHealth(self):
        endpointURL = self.NODE_URL + "health-check"
        response = requests.get(endpointURL)
        return response

    def getExchangeRate(self):
        '''Returns Deso Price'''
        endpointURL = self.NODE_URL + "get-exchange-rate"
        response = requests.get(endpointURL)
        return response

    def getAppState(self):
        '''Returns App State that includes current block height, deso price and other node related data'''
        payload = {"PublicKeyBase58Check": self.PUBLIC_KEY}

        endpointURL = self.NODE_URL + "get-app-state"
        response = requests.post(endpointURL, json=payload)
        return response

    def getDiamondLevelMap(self, inDesoNanos = True):
        '''Returns Diamond Level Map. set inDesoNanos = False to get in Deso'''
        if inDesoNanos:
            return {
                "1": 50000, "2": 500000, "3": 5000000, "4": 50000000, "5": 500000000, "6": 5000000000, "7": 50000000000, "8": 500000000000
            }
        
        else:
            return{
             "1": 0.00005, "2": 0.0005, "3": 0.005, "4": 0.05, "5": 0.5, "6": 5, "7": 50, "8": 500
        }
