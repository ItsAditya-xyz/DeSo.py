import requests
from deso.Route import getRoute
from deso.Sign import Sign_Transaction
import binascii
from ecdsa import SigningKey, SECP256k1
from ecdsa.ecdsa import Public_key
import jwt

class Post:
    def __init__(self, seedHex, publicKey):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey

    def uploadImage(self, fileList):
        ROUTE = getRoute()
        private_key = bytes(self.SEED_HEX, 'utf-8')
        private_key = binascii.unhexlify(private_key)
        key = SigningKey.from_string(private_key, curve=SECP256k1)
        key = key.to_pem()
        encoded_jwt = jwt.encode({}, key, algorithm="ES256")
        # print(encoded_jwt)
        endpointURL = ROUTE + "upload-image"
        payload = {'UserPublicKeyBase58Check': self.PUBLIC_KEY,
                   'JWT': encoded_jwt}
        response = requests.request("POST", endpointURL, data=payload, files=fileList)
        return response.text


    def send(self, content, imageUrl=[], postExtraData={}):
        header = {
            "content-type": "application/json"
        }

        payload = {"UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                "PostHashHexToModify": "",
                "ParentStakeID": "",
                "Title": "",
                "BodyObj": {"Body": content, "ImageURLs": imageUrl},
                "RecloutedPostHashHex": "",
                "PostExtraData": postExtraData,
                "Sub": "",
                "IsHidden":  False,
                "MinFeeRateNanosPerKB": 1000
                }
        ROUTE = getRoute()
        endpointURL = ROUTE + "submit-post"
        res = requests.post(endpointURL, json=payload, headers=header)
        transactionHex = res.json()["TransactionHex"]

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return {"status":submitResponse.status_code , "postHashHex": submitResponse.json()["TxnHashHex"]} # returns 200

    def mint(self, postHashHex, minBidDeSo,  copy=1, creatorRoyality=5, coinHolderRoyality=10, isForSale=True):
            ROUTE = getRoute()
            endpointURL = ROUTE + "create-nft"
            payload = {"UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                        "NFTPostHashHex": postHashHex,
                        "NumCopies": copy,
                        "NFTRoyaltyToCreatorBasisPoints": round(creatorRoyality*100),
                        "NFTRoyaltyToCoinBasisPoints": round(coinHolderRoyality*10), 
                        "HasUnlockable": False, 
                        "IsForSale": isForSale, "MinBidAmountNanos": round( minBidDeSo * 1e9),
                        "MinFeeRateNanosPerKB": 1000}
            response = requests.post(endpointURL, json=payload)
            transactionHex = response.json()["TransactionHex"]
            signedTransactionHex = Sign_Transaction(
                self.SEED_HEX, transactionHex
            )  # txn signature

            submitPayload = {"TransactionHex": signedTransactionHex}
            endpointURL = ROUTE + "submit-transaction"
            submitResponse = requests.post(endpointURL, json=submitPayload)
            return submitResponse.status_code  # returns 200 if buy is succesful
