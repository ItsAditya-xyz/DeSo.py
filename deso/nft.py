import pathlib

import arweave
from arweave.arweave_lib import Transaction
from arweave.transaction_uploader import get_uploader

from .base import BaseClient
from .endpoints import ENDPOINTS


class NFT(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def get_nft(self, post_hash_hex):
        # Route
        route = ENDPOINTS["get-nft-entries"]

        # Payload
        payload = {
            "ReaderPublicKeyBase58Check": "BC1YLiwBkXtiG4cf4k4o1VdZHEWT4Caew7HrQ9cKAba5ng5Nev1md1z",
            "PostHashHex": post_hash_hex,
        }

        # Fetch and return
        _, json = self.fetch_api(route, body=payload)

        return json

    def upload_to_arweave(self, wallet, image):
        # Wallet
        wallet = arweave.Wallet(wallet)

        # Upload
        with open(image, "rb", buffering=0) as file_handler:
            # Create transaction
            tx = Transaction(wallet, file_handler=file_handler, file_path=image)

            # Get file exist
            file_extension = pathlib.Path(image).suffix
            type = str(file_extension[1:])

            # Add tags and sign
            tx.add_tag("Content-Type", "image/" + type)
            tx.sign()

            # Upload
            uploader = get_uploader(tx, file_handler)
            while not uploader.is_complete:
                uploader.upload_chunk()

            # Send
            tx.send()
            image_id = str(tx.id)
            transaction_id = wallet.get_last_transaction_id()

            # Build URL
            build_url = f"https://{transaction_id[1:]}.arweave.net/{image_id}"
            return build_url
