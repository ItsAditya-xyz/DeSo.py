import requests
from deso.Route import getRoute
from deso.Sign import Sign_Transaction


class Message:
    def __init__(self, seedHex, publicKey):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey

    def send(self, recipient, messageText):
        header = {
            "content-type": "application/json"
        }

        payload = {"SenderPublicKeyBase58Check":self.PUBLIC_KEY,"RecipientPublicKeyBase58Check":recipient,"MessageText":messageText,"MinFeeRateNanosPerKB":1000}
        ROUTE = getRoute()
        endpointURL = ROUTE + "send-message-stateless"
        res = requests.post(endpointURL, json=payload, headers=header)
        transactionHex = res.json()["TransactionHex"]

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if buy is succesful