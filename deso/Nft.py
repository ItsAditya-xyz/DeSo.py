import requests
import json
from deso.Route import getRoute
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
import arweave
import logging
import pathlib
from deso.Sign import Sign_Transaction


class Nft:
    def __init__(self, seedHex, publicKey):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey

    def getNFT(postHashHex):
        payload = {"ReaderPublicKeyBase58Check": "BC1YLiwBkXtiG4cf4k4o1VdZHEWT4Caew7HrQ9cKAba5ng5Nev1md1z",
                   "PostHashHex": postHashHex}
        ROUTE = getRoute()
        endpointURL = ROUTE + "get-nft-entries-for-nft-post"
        response = requests.post(endpointURL, json=payload)
        return response.json()

    def uploadToArweave(wallet, image):
        wallet = arweave.Wallet(wallet)
        with open(image, "rb", buffering=0) as file_handler:
            tx = Transaction(
                wallet,  file_handler=file_handler, file_path=image)
            file_extension = pathlib.Path(image).suffix
            type = str(file_extension[1:])
            tx.add_tag('Content-Type', 'image/' + type)
            tx.sign()
            uploader = get_uploader(tx, file_handler)
            while not uploader.is_complete:
                uploader.upload_chunk()
            tx.send()
            image_id = str(tx.id)
            transaction_id = wallet.get_last_transaction_id()
            build_url = 'https://' + \
                transaction_id[1:] + '.arweave.net/' + image_id
            return build_url

  