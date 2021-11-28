from .base import BaseClient
from .endpoints import ENDPOINTS
from .sign import sign_transaction


class Message(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def send(self, recipient, text):
        # Header
        header = {"content-type": "application/json"}

        # Payload
        payload = {
            "SenderPublicKeyBase58Check": self.public_key,
            "RecipientPublicKeyBase58Check": recipient,
            "MessageText": text,
            "MinFeeRateNanosPerKB": 1000,
        }

        # Send message stateless
        route = ENDPOINTS["send-message-stateless"]
        transaction_hex = self.fetch_api(route, headers=header, body=payload)[
            "TransactionHex"
        ]

        # Sign transaction
        signed_transaction_hex = sign_transaction(self.seed_hex, transaction_hex)

        # Submit transaction
        route = ENDPOINTS["submit-transaction"]
        code, _ = self.fetch_api(
            route, headers=header, body={"TransactionHex": signed_transaction_hex}
        )

        return code
