import requests
import json
from deso.Route import getRoute

class Nft:
    def  getNFT(postHashHex):
        payload = {"ReaderPublicKeyBase58Check":"BC1YLiwBkXtiG4cf4k4o1VdZHEWT4Caew7HrQ9cKAba5ng5Nev1md1z","PostHashHex":postHashHex}
        ROUTE = getRoute()
        endpointURL = ROUTE + "get-nft-entries-for-nft-post"
        response = requests.post(endpointURL, json = payload)
        return response.json()

    
