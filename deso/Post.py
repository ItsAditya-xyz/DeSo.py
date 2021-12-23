from os import PathLike
import requests
from deso.Route import getRoute
from deso.Sign import Sign_Transaction
from deso.Derived import addExtraData
import binascii
from ecdsa import SigningKey, SECP256k1
from ecdsa.ecdsa import Public_key
import jwt


class Post:
    def __init__(self, seedHex=None, publicKey=None):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.MIN_FEE = 1000
        self.DERIVED_KEY = None

    def useDerivedKey(self, publicKey, derivedKey, derivedSeedHex):
        self.PUBLIC_KEY = publicKey
        self.DERIVED_KEY = derivedKey
        self.SEED_HEX = derivedSeedHex
        # If using derived keys set min fee rate to 1250 bc transaction fails at default value
        self.MIN_FEE = 1250

    def uploadImage(self, fileList):
        # If the user passed the path to a simgle image, convert string into useable list
        # I dont wanna make a list everytime I just want to upload a single image T_T
        if type(fileList) == type("str"):
            fileList = [
                ('file', (fileList, open(
                    fileList, "rb"), 'image/png'))
            ]
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
        if self.DERIVED_KEY:
            payload["UserPublicKeyBase58Check"] = self.DERIVED_KEY
        response = requests.request(
            "POST", endpointURL, data=payload, files=fileList)
        return response.json()

    def send(self, content, imageUrl=[], postExtraData={}):
        # if user passed url for a single image as string, convert str into list[str]
        if type(imageUrl) == type("str"):
            imageUrl = [imageUrl]
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
                   "MinFeeRateNanosPerKB": self.MIN_FEE
                   }
        ROUTE = getRoute()
        endpointURL = ROUTE + "submit-post"
        res = requests.post(endpointURL, json=payload, headers=header)
        transactionHex = res.json()["TransactionHex"]

        if self.DERIVED_KEY:
            transactionHex = addExtraData(transactionHex, self.DERIVED_KEY)

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        if submitResponse.status_code == 200:
            return {"status": submitResponse.status_code, "postHashHex": submitResponse.json()["TxnHashHex"]}
        else:
            return submitResponse.json()

    def mint(self, postHashHex, minBidDeSo,  copy=1, creatorRoyality=5, coinHolderRoyality=10, isForSale=True):
        ROUTE = getRoute()
        endpointURL = ROUTE + "create-nft"
        payload = {"UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                   "NFTPostHashHex": postHashHex,
                   "NumCopies": copy,
                   "NFTRoyaltyToCreatorBasisPoints": round(creatorRoyality*100),
                   "NFTRoyaltyToCoinBasisPoints": round(coinHolderRoyality*100),
                   "HasUnlockable": False,
                   "IsForSale": isForSale, "MinBidAmountNanos": round(minBidDeSo * 1e9),
                   "MinFeeRateNanosPerKB": self.MIN_FEE}

        response = requests.post(endpointURL, json=payload)
        transactionHex = response.json()["TransactionHex"]

        if self.DERIVED_KEY:
            transactionHex = addExtraData(transactionHex, self.DERIVED_KEY)

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if mint is succesful

    # write transactions on posts goes here
    def like(self, postHashHex, isLike=True):
        ROUTE = getRoute()
        endpointURL = ROUTE + "create-like-stateless"
        payload = {"ReaderPublicKeyBase58Check": self.PUBLIC_KEY,
                   "LikedPostHashHex": postHashHex,
                   "IsUnlike": not isLike,
                   "MinFeeRateNanosPerKB": self.MIN_FEE}

        response = requests.post(endpointURL, json=payload)
        transactionHex = response.json()["TransactionHex"]

        if self.DERIVED_KEY:
            transactionHex = addExtraData(transactionHex, self.DERIVED_KEY)

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        return submitResponse.status_code  # returns 200 if like is succesful
