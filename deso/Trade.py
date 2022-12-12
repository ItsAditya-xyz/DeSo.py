import requests
from deso.utils import submitTransaction, appendExtraData
from deso.Sign import Sign_Transaction

NODES = [
    'https://node.deso.org/api/v0/',
    'https://love4src.com/api/v0/',
]


class Trade:
    def __init__(
        self,
        publicKey,
        seedHex=None,
        nodeURL=NODES[0],
        derivedPublicKey=None,
        derivedSeedHex=None,
        minFee=1000,
        derivedKeyFee=1700,
    ):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL
        self.DERIVED_PUBLIC_KEY = derivedPublicKey
        self.DERIVED_SEED_HEX = derivedSeedHex
        self.MIN_FEE = minFee if seedHex else derivedKeyFee

    def sendDeso(self, recieverPublicKeyOrUsername, desoToSend):

        error = None
        endpointURL = self.NODE_URL + "send-deso"
        payload = {
            "SenderPublicKeyBase58Check": self.PUBLIC_KEY,
            "RecipientPublicKeyOrUsername": recieverPublicKeyOrUsername,
            "AmountNanos": int(round(desoToSend * 1e9)),
            "MinFeeRateNanosPerKB": self.MIN_FEE,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "send-deso"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def buyCreatorCoin(self, creatorPublicKey, desoAmountToBuy):

        error = None
        endpointURL = self.NODE_URL + "buy-or-sell-creator-coin"
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "CreatorPublicKeyBase58Check": creatorPublicKey,
            "OperationType": "buy",
            "DeSoToSellNanos": int(desoAmountToBuy * 1e9),
            "CreatorCoinToSellNanos": 0,
            "DeSoToAddNanos": 0,
            "MinDeSoExpectedNanos": 0,
            "MinCreatorCoinExpectedNanos": 0,
            "MinFeeRateNanosPerKB": self.MIN_FEE,
            "InTutorial": False,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "buy-or-sell-creator-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def getHeldCoinsOfCreator(self, publicKeyOfCoin):
        endpointURL = self.NODE_URL + "get-users-stateless"
        payload = {"PublicKeysBase58Check": [self.PUBLIC_KEY]}
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "get-users-stateless"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

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
        beforeFees = desoLockedNanos * (
            1 - pow((1 - balanceNanos / coinsInCirculation), (1 / 0.3333333))
        )
        try:
            amount = (beforeFees * (100 * 100 - 1)) / (100 * 100)
        except Exception:
            amount = 0
        return amount

    def sellCreatorCoin(self, creatorPublicKey, coinsToSellNanos):
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
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "buy-or-sell-creator-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def sendCreatorCoins(
        self,
        creatorPublicKey,
        receiverUsernameOrPublicKey,
        creatorCoinNanosToSend,
    ):

        error = None
        endpointURL = self.NODE_URL + "transfer-creator-coin"
        payload = {
            "SenderPublicKeyBase58Check":
                self.PUBLIC_KEY,
            "CreatorPublicKeyBase58Check":
                creatorPublicKey,
            "ReceiverUsernameOrPublicKeyBase58Check":
                receiverUsernameOrPublicKey,
            "CreatorCoinToTransferNanos":
                creatorCoinNanosToSend,
            "MinFeeRateNanosPerKB":
                self.MIN_FEE,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "transfer-creator-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])
        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def sendDAOCoins(
        self, coinsToTransfer, daoPublicKeyOrName, receiverPublicKeyOrUsername
    ):
        """
        Sends DAO coin to publicKey or username. Use the hex() function to
        convert a number to hexadecimal for Example,
        if you want to send 15 DAO coin, set coinsToTransfer to
        hex(int(15*1e18))
        """

        error = None
        endpointURL = self.NODE_URL + "transfer-dao-coin"
        payload = {
            "SenderPublicKeyBase58Check":
                self.PUBLIC_KEY,
            "ProfilePublicKeyBase58CheckOrUsername":
                daoPublicKeyOrName,
            "ReceiverPublicKeyBase58CheckOrUsername":
                receiverPublicKeyOrUsername,
            "DAOCoinToTransferNanos":
                str(coinsToTransfer),
            "MinFeeRateNanosPerKB":
                self.MIN_FEE,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "transfer-dao-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def burnDAOCoins(self, coinsToBurn, daoPublicKeyOrName):
        """
        Burns DAO coin of daoPublicKeyOrName. Use the hex() function to
        convert a number to hexadecimal for Example,
        if you want to burn 15 DAO coin, set coinsToBurn to hex(int(15*1e18))
        """
        error = None
        endpointURL = self.NODE_URL + "dao-coin"
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "ProfilePublicKeyBase58CheckOrUsername": daoPublicKeyOrName,
            "OperationType": "burn",
            "CoinsToBurnNanos": coinsToBurn,
            "MinFeeRateNanosPerKB": self.MIN_FEE,
        }

        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "dao-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the transactions."
                    " Make sure publicKey and seedHex are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse

    def mintDAOCoins(self, coinsToMint):
        """
        Mint DAO coins. Use the hex() function to convert a number to
        hexadecimal for Example,
        if you want to mint 15 DAO coin, set coinsToBurn to hex(int(15*1e18))
        """

        error = None
        endpointURL = self.NODE_URL + "dao-coin"
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "ProfilePublicKeyBase58CheckOrUsername": self.PUBLIC_KEY,
            "OperationType": "mint",
            "CoinsToMintNanos": coinsToMint,
            "MinFeeRateNanosPerKB": self.MIN_FEE,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "dao-coin"
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        error = response.json()
        transactionHex = response.json()["TransactionHex"]
        if (
            self.DERIVED_PUBLIC_KEY is not None
            and self.DERIVED_SEED_HEX is not None
            and self.SEED_HEX is None
        ):
            extraDataResponse = appendExtraData(
                transactionHex, self.DERIVED_PUBLIC_KEY, self.NODE_URL
            )
            error = extraDataResponse.json()
            transactionHex = extraDataResponse.json()["TransactionHex"]
        seedHexToSignWith = (
            self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
        )
        try:
            signedTransactionHex = Sign_Transaction(
                seedHexToSignWith, transactionHex
            )
        except Exception as e:
            error = {
                "error":
                    "Something went wrong while signing the "
                    "transactions. Make sure publicKey and seedHex "
                    "are correct."
            }
            raise e(error["error"])

        submitTransactionResponse = submitTransaction(
            signedTransactionHex, self.NODE_URL
        )
        return submitTransactionResponse
