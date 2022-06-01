from deso.utils import submitTransaction, appendExtraData
import requests
from deso.Sign import Sign_Transaction


class Trade:
    def __init__(self, publicKey, seedHex=None,  nodeURL="https://node.deso.org/api/v0/", derivedPublicKey=None, derivedSeedHex=None, minFee=1000, derivedKeyFee=1700):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL
        self.DERIVED_PUBLIC_KEY = derivedPublicKey
        self.DERIVED_SEED_HEX = derivedSeedHex
        self.MIN_FEE = minFee if seedHex else derivedKeyFee

    def sendDeso(self, recieverPublicKeyOrUsername, desoToSend):
        try:
            error = None
            endpointURL = self.NODE_URL + "send-deso"
            payload = {"SenderPublicKeyBase58Check": self.PUBLIC_KEY,
                       "RecipientPublicKeyOrUsername": recieverPublicKeyOrUsername,
                       "AmountNanos": int(round(desoToSend*1e9)),
                       "MinFeeRateNanosPerKB": self.MIN_FEE}
            response = requests.post(endpointURL, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            if self.DERIVED_PUBLIC_KEY is not None and self.DERIVED_SEED_HEX is not None and self.SEED_HEX is None:
                extraDataResponse = appendExtraData(
                    transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL)
                error = extraDataResponse.json()
                transactionHex = extraDataResponse.json()["TransactionHex"]
            seedHexToSignWith = self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex)
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])

    def buyCreatorCoin(self, creatorPublicKey, desoAmountToBuy):
        try:
            error = None
            endpointURL = self.NODE_URL + "buy-or-sell-creator-coin"
            payload = {"UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                       "CreatorPublicKeyBase58Check": creatorPublicKey,
                       "OperationType": "buy",
                       "DeSoToSellNanos": int(desoAmountToBuy * 1e9),
                       "CreatorCoinToSellNanos": 0,
                       "DeSoToAddNanos": 0,
                       "MinDeSoExpectedNanos": 0,
                       "MinCreatorCoinExpectedNanos": 0,
                       "MinFeeRateNanosPerKB": self.MIN_FEE,
                       "InTutorial": False}
            response = requests.post(endpointURL, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            if self.DERIVED_PUBLIC_KEY is not None and self.DERIVED_SEED_HEX is not None and self.SEED_HEX is None:
                extraDataResponse = appendExtraData(
                    transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL)
                error = extraDataResponse.json()
                transactionHex = extraDataResponse.json()["TransactionHex"]
            seedHexToSignWith = self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex)
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])

    def getHeldCoinsOfCreator(self, publicKeyOfCoin):
        endpoint = self.NODE_URL + "get-users-stateless"
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

    def amountOnSell(desoLockedNanos, coinsInCirculation, balanceNanos):
        beforeFees = desoLockedNanos * \
            (1 - pow((1-balanceNanos/coinsInCirculation), (1 / 0.3333333)))
        return ((beforeFees * (100*100 - 1)) / (100*100))

    def sellCreatorCoin(self, creatorPublicKey, coinsToSellNanos):
        try:
            endpointURL = self.NODE_URL + "buy-or-sell-creator-coin"
            payload = {
                "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                "CreatorPublicKeyBase58Check": creatorPublicKey,
                "OperationType": "sell",
                "DeSoToSellNanos": 0,
                "CreatorCoinToSellNanos": coinsToSellNanos,
                "DeSoToAddNanos": 0,
                "MinDeSoExpectedNanos": 0,
                "MinCreatorCoinExpectedNanos": 0,
                "MinFeeRateNanosPerKB": 1000,
            }
            response = requests.post(endpointURL, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            if self.DERIVED_PUBLIC_KEY is not None and self.DERIVED_SEED_HEX is not None and self.SEED_HEX is None:
                extraDataResponse = appendExtraData(
                    transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL)
                error = extraDataResponse.json()
                transactionHex = extraDataResponse.json()["TransactionHex"]
            seedHexToSignWith = self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex)
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])

    def sendCreatorCoins(self, creatorPublicKey, receiverUsernameOrPublicKey, creatorCoinNanosToSend):
        try:
            error = None
            endpointURL = self.NODE_URL + "transfer-creator-coin"
            payload = {"SenderPublicKeyBase58Check": self.PUBLIC_KEY,
                       "CreatorPublicKeyBase58Check": creatorPublicKey,
                       "ReceiverUsernameOrPublicKeyBase58Check": receiverUsernameOrPublicKey,
                       "CreatorCoinToTransferNanos": creatorCoinNanosToSend,
                       "MinFeeRateNanosPerKB": self.MIN_FEE}
            response = requests.post(endpointURL, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            if self.DERIVED_PUBLIC_KEY is not None and self.DERIVED_SEED_HEX is not None and self.SEED_HEX is None:
                extraDataResponse = appendExtraData(
                    transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL)
                error = extraDataResponse.json()
                transactionHex = extraDataResponse.json()["TransactionHex"]
            seedHexToSignWith = self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex)
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])

    def sendDAOCoins(self,  coinsToTransfer, daoPublicKeyOrName, receiverPublicKeyOrUsername):
        '''Sends DAO coin to publicKey or username. Use the hex() function to convert a number to hexadecimal
        for Example, if you want to send 15 DAO coin, set coinsToTransferNanosInHex to hex(int(15*1e18))'''
        try:
            error = None
            endpointURL = self.NODE_URL + "transfer-dao-coin"
            payload = {"SenderPublicKeyBase58Check": self.PUBLIC_KEY,
                       "ProfilePublicKeyBase58CheckOrUsername": daoPublicKeyOrName,
                       "ReceiverPublicKeyBase58CheckOrUsername": receiverPublicKeyOrUsername,
                       "DAOCoinToTransferNanos": str(coinsToTransfer),
                       "MinFeeRateNanosPerKB": self.MIN_FEE}

            response = requests.post(endpointURL, json=payload)
            error = response.json()
            transactionHex = response.json()["TransactionHex"]
            if self.DERIVED_PUBLIC_KEY is not None and self.DERIVED_SEED_HEX is not None and self.SEED_HEX is None:
                extraDataResponse = appendExtraData(
                    transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL)
                error = extraDataResponse.json()
                transactionHex = extraDataResponse.json()["TransactionHex"]
            seedHexToSignWith = self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex)
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."}
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL)
            return submitTransactionResponse
        except Exception as e:
            raise Exception(error["error"])
