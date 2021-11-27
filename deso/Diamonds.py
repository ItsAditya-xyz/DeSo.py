import requests
import json
from deso.Route import getRoute


class Diamonds:
    def getDiamonds(publicKey, received=True):
        """when received is false, it returns the diamonds info which is given by the user."""
        payload = {"PublicKeyBase58Check": publicKey, "FetchYouDiamonded": not received}
        route = getRoute()
        endpointURL = route + "get-diamonds-for-public-key"
        response = requests.post(endpointURL, json=payload)
        return response.json()
