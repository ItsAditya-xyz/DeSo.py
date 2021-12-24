from deso.Route import getRoute
import json
import requests
from deso.Sign import Sign_Transaction
import base58
from deso.Derived import addExtraDataDict


class Deso:
    def __init__(self, PUBLIC_KEY=None, SEEDHEX=None, DERIVED_KEY=None):
        self.PUBLIC_KEY = PUBLIC_KEY
        self.SEEDHEX = SEEDHEX
        self.DERIVED_KEY = DERIVED_KEY

    def getDeSoPrice(self):  # returns deso price
        response = requests.get(
            "https://api.blockchain.com/v3/exchange/tickers/CLOUT-USD")
        return response.json()

    def getCurrentBlock(self):
        endpoint = getRoute()+"get-app-state"
        res = requests.post(endpoint, {})
        return res.json()["BlockHeight"]

    def usdToNanos(self, amount_usd: int):
        one_deso_in_usd = self.getDeSoPrice()["last_trade_price"]
        amount_usd_in_deso = amount_usd/one_deso_in_usd
        amount_usd_in_nano = amount_usd_in_deso*(10**9)
        return amount_usd_in_nano

    def basicTransfer(self, recipientPublicKey, amountDeSo, extraData: dict = {}):
        endpoint = getRoute() + "send-deso"
        payload = {
            "SenderPublicKeyBase58Check": self.PUBLIC_KEY,
            "RecipientPublicKeyOrUsername": recipientPublicKey,
            "AmountNanos": int(round(amountDeSo * 1e9)),
            "MinFeeRateNanosPerKB": 1000
        }

        if self.DERIVED_KEY:
            # below this transaction failed
            payload["MinFeeRateNanosPerKB"] = 1500

        res = requests.post(endpoint, json=payload)
        TransactionHex = res.json()["TransactionHex"]

        if self.DERIVED_KEY:
            compressed_key = base58.b58decode_check(self.DERIVED_KEY)[3:].hex()
            extraData["DerivedPublicKey"] = compressed_key
        if not extraData == {}:
            TransactionHex = addExtraDataDict(TransactionHex, extraData)

        SignedTransactionHex = Sign_Transaction(self.SEEDHEX, TransactionHex)
        payload = {"TransactionHex": SignedTransactionHex}
        endpoint = getRoute() + "submit-transaction"
        res = requests.post(endpoint, json=payload)
        # print(res.json())
        return {"status": res.status_code}
