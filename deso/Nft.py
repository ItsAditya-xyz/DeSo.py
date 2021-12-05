import requests
import json

from requests.models import Response
from deso.Route import ROUTE, getRoute
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

    def updateNFT(self, postHashHex: str, min_bid_deso: int = 1, for_sale: bool = True, serial_number: int = 1):
        header = {"content-type": "application/json"}
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "NFTPostHashHex": postHashHex,
            "SerialNumber": serial_number,
            "IsForSale": for_sale,
            "MinBidAmountNanos": min_bid_deso//1e9,  # convert DESO to NANOS
            "MinFeeRateNanosPerKB": 1000
        }

        endpointURL = ROUTE() + "update-nft"
        response = requests.post(endpointURL, json=payload, headers=header)
        if response.status_code == 200:
            transactionHex = response.json()["TransactionHex"]
            signedTransactionHex = Sign_Transaction(
                self.SEEDHEX, transactionHex)
            submitPayload = {"TransactionHex": signedTransactionHex}
            submitResponse = requests.post(
                ROUTE()+"submit-transaction", json=submitPayload)

            return submitResponse.json()
        else:
            return response.json()

    def burnNFT(self, postHashHex, serial_number: int = 1):
        # ONLY NFTS THAT ARE NOT ON SALE CAN BE BURNED
        header = {"content-type": "application/json"}
        payload = {
            "UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
            "NFTPostHashHex": postHashHex,
            "SerialNumber": serial_number,
            "MinFeeRateNanosPerKB": 1000
        }

        endpointURL = ROUTE()+"burn-nft"
        response = requests.post(endpointURL, json=payload, headers=header)

        if response.status_code == 200:
            transactionHex = response.json()["TransactionHex"]
            signedTransactionHex = Sign_Transaction(
                self.SEEDHEX, transactionHex)
            submitPayload = {"TransactionHex": signedTransactionHex}
            submitResponse = requests.post(
                ROUTE()+"submit-transaction", json=submitPayload)

            return submitResponse.json()
        else:
            return response.json()
