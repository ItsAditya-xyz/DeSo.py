import requests
import json
from deso.Route import getRoute
from deso.Sign import Sign_Transaction


class Trade:
    def __init__(self, seedHex, publicKey):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey

    def buy(self, keyToBuy, DeSo):
        print(self.SEED_HEX)
        DeSoNanos = int(DeSo * (10 ** 9))
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "CreatorPublicKeyBase58Check": keyToBuy,
            "OperationType": "buy",
            "BitCloutToSellNanos": DeSoNanos,
            "CreatorCoinToSellNanos": 0,
            "BitCloutToAddNanos": 0,
            "MinBitCloutExpectedNanos": 0,
            "MinCreatorCoinExpectedNanos": 10,
            "MinFeeRateNanosPerKB": 1000,
        }
        ROUTE = getRoute()
        endpointURL = ROUTE + "buy-or-sell-creator-coin"
        res = requests.post(endpointURL, json=payload)
        transactionHex = res.json()["TransactionHex"]

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if buy is succesful

        # if someone has time pls, add some meaningul try catch blocks and error messages. i will def tip you

    def getMaxCoins(self, publicKeyOfCoin):
        ROUTE = getRoute()
        endpoint = ROUTE + "get-users-stateless"
        payload = {"PublicKeysBase58Check": [self.PUBLIC_KEY]}
        response = requests.post(endpoint, json=payload)
        hodlings = response.json()["UserList"][0]["UsersYouHODL"]
        for hodling in hodlings:
            if hodling["CreatorPublicKeyBase58Check"] == publicKeyOfCoin:
                coinsHeld = hodling["BalanceNanos"]
                if coinsHeld != 0:
                    return hodling["BalanceNanos"]
                else:
                    return -1
        return -1

    def amountOnSell(bitcloutLockedNanos, coinsInCirculation, balanceNanos):
        beforeFees = bitcloutLockedNanos * (
            1 - pow((1 - balanceNanos / coinsInCirculation), (1 / 0.3333333))
        )
        return (beforeFees * (100 * 100 - 1)) / (100 * 100)

    def sell(self, keyToSell, coinsToSellNanos=0, sellMax=False):
        coinsToSell = coinsToSellNanos
        if sellMax == True:
            maxCoins = Trade.getMaxCoins(self, publicKeyOfCoin=keyToSell)
            if maxCoins == -1:
                print("You don't hodl that creator")
                return 404
            else:
                coinsToSell = maxCoins

        ROUTE = getRoute()
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "CreatorPublicKeyBase58Check": keyToSell,
            "OperationType": "sell",
            "BitCloutToSellNanos": 0,
            "CreatorCoinToSellNanos": coinsToSell,
            "BitCloutToAddNanos": 0,
            "MinBitCloutExpectedNanos": 0,
            "MinCreatorCoinExpectedNanos": 0,
            "MinFeeRateNanosPerKB": 1000,
        }
        endpointURL = ROUTE + "buy-or-sell-creator-coin"
        res = requests.post(endpointURL, json=payload)
        transactionHex = res.json()["TransactionHex"]
        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if sell is succesful
