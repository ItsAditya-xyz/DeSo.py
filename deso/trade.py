from .base import BaseClient
from .endpoints import ENDPOINTS
from .sign import sign_transaction


class Trade(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    @staticmethod
    def amount_on_sell(bitclout_locked_nanos, coins_in_circulation, balance_nanos):
        before_fees = bitclout_locked_nanos * (
            1 - pow((1 - balance_nanos / coins_in_circulation), (1 / 0.3333333))
        )
        return (before_fees * (100 * 100 - 1)) / (100 * 100)

    def get_max_coins(self, public_key_of_coin):
        # Payload
        payload = {"PublicKeysBase58Check": [self.public_key]}

        # Route
        route = ENDPOINTS["get-users-stateless"]

        # Make request
        json = self.fetch_api(route, body=payload)

        # Parse
        hodlings = json["UserList"][0]["UsersYouHODL"]

        # Iteration through list
        for hodling in hodlings:
            if hodling["CreatorPublicKeyBase58Check"] == public_key_of_coin:
                coins_held = hodling["BalanceNanos"]

                if coins_held != 0:
                    return hodling["BalanceNanos"]
                else:
                    return -1
        return -1

    # Buy function
    def buy(self, key_to_buy, deso):
        # Calculate nanos
        deso_nanos = int(deso * (10 ** 9))

        # Generate request payload
        payload = {
            "UpdaterPublicKeyBase58Check": self.public_key,
            "CreatorPublicKeyBase58Check": key_to_buy,
            "OperationType": "buy",
            "BitCloutToSellNanos": deso_nanos,
            "CreatorCoinToSellNanos": 0,
            "BitCloutToAddNanos": 0,
            "MinBitCloutExpectedNanos": 0,
            "MinCreatorCoinExpectedNanos": 10,
            "MinFeeRateNanosPerKB": 1000,
        }

        # Get route
        route = ENDPOINTS["buy-or-sell-creator-coin"]

        # Make request
        transaction_hex = self.fetch_api(route, body=payload)["TransactionHex"]

        # Sign transaction
        signed_transaction_hex = sign_transaction(self.seed_hex, transaction_hex)

        # Submit transaction
        submit_payload = {"TransactionHex": signed_transaction_hex}
        route = ENDPOINTS["submit-transaction"]
        code, _ = self.fetch_api(route, body=submit_payload)

        return code

    # Sell
    def sell(self, key_to_sell, coins_to_sell_nanos=0, sell_max=False):
        coins_to_sell = coins_to_sell_nanos

        if sell_max:
            max_coins = self.get_max_coins(key_to_sell)

            if max_coins == -1:
                print("You don't hodl that creator")
                return 404
            else:
                coins_to_sell = max_coins

        # Payload
        payload = {
            "UpdaterPublicKeyBase58Check": self.public_key,
            "CreatorPublicKeyBase58Check": key_to_sell,
            "OperationType": "sell",
            "BitCloutToSellNanos": 0,
            "CreatorCoinToSellNanos": coins_to_sell,
            "BitCloutToAddNanos": 0,
            "MinBitCloutExpectedNanos": 0,
            "MinCreatorCoinExpectedNanos": 0,
            "MinFeeRateNanosPerKB": 1000,
        }

        # Get route
        route = ENDPOINTS["buy-or-sell-creator-coin"]

        # Make request
        transaction_hex = self.fetch_api(route, body=payload)["TransactionHex"]

        # Sign transaction
        signed_transaction_hex = sign_transaction(self.seed_hex, transaction_hex)

        # Submit transaction
        submit_payload = {"TransactionHex": signed_transaction_hex}
        route = ENDPOINTS["submit-transaction"]
        code, _ = self.fetch_api(route, body=submit_payload)

        return code
