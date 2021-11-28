import binascii

from .base import BaseClient
from .endpoints import ENDPOINTS
from .Sign import Sign_Transaction

import jwt
from ecdsa import SigningKey, SECP256k1


class Message(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def upload_image(self, file_list):
        # Private key
        private_key = bytes(self.SEED_HEX, "utf-8")
        private_key = binascii.unhexlify(private_key)

        # Key
        key = SigningKey.from_string(private_key, curve=SECP256k1)
        key = key.to_pem()

        # Encoded JWT
        encoded_jwt = jwt.encode({}, key, algorithm="ES256")

        # Payload
        payload = {"UserPublicKeyBase58Check": self.public_key, "JWT": encoded_jwt}

        # Upload-image endpoint
        route = ENDPOINTS["upload-image"]

        # Make req, and return text
        return self.fetch_api(route, body=payload, files=file_list, text=True)


    def send(self, content, image_url=None, post_extra_data=None):
        if not image_url:
            image_url = []

        if not post_extra_data:
            post_extra_data = {}

    def mint(
        self,
        post_hash_hex,
        min_bid_deso,
        copy=1,
        creator_royalty=5,
        coin_holder_royalty=10,
        is_for_sale=True,
    ):
        ...
