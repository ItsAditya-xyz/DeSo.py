import requests
from deso.utils import submitTransaction
import requests
from deso.Sign import Sign_Transaction


class Derived:
    # takes two optional Argument; publicKey and nodeURL. By default NodeURL is https://node.deso.org/api/v0/"
    def __init__(self, nodeURL="https://node.deso.org/api/v0/",  minFee=1000):
        self.NODE_URL = nodeURL
        self.MIN_FEE = minFee

    def authorizeDerivedKey(self, publicKey, derivedPublicKey, derivedSeedHex, expirationBlock, accessSignature, transactionSpendingLimitHex, derivedKeySignature=True, isAuth=True):
        try:
            error = None
            payload = {
                "OwnerPublicKeyBase58Check": publicKey,
                "DerivedPublicKeyBase58Check": derivedPublicKey,
                "ExpirationBlock": expirationBlock,
                "AccessSignature": accessSignature,
                "DeleteKey": not isAuth,
                "DerivedKeySignature": derivedKeySignature,
                "transactionSpendingLimitHex": transactionSpendingLimitHex,
                "MinFeeRateNanosPerKB": self.MIN_FEE,

            }
            endpoint = self.NODE_URL + "authorize-derived-key"
            response = requests.post(endpoint, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            try:
                signedTransactionHex = Sign_Transaction(
                    derivedSeedHex, transactionHex
                )  # txn signature
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure public key, derived key and derivedSeedHex are correct.\nAlso, Make sure the derived Key hasAUTHORIZE_DERIVED_KEY permission as well"}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])
