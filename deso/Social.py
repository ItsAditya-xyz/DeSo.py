import requests
import json
from deso.Route import getRoute
from deso.Sign import Sign_Transaction


class Social:
    def __init__(self, seedHex, publicKey):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey

    def follow(self, publicKeyToFollow, isUnfollow=False):

        payload = {"FollowerPublicKeyBase58Check": self.PUBLIC_KEY,
                   "FollowedPublicKeyBase58Check": publicKeyToFollow, "IsUnfollow": isUnfollow, "MinFeeRateNanosPerKB": 1000}
        ROUTE = getRoute()
        endpointURL = ROUTE + "create-follow-txn-stateless"
        res = requests.post(endpointURL, json=payload)
        transactionHex = res.json()["TransactionHex"]

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if follow/unfollow is succesful
