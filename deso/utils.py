import requests
import jwt
import binascii
from base58 import b58decode_check
from ecdsa import SECP256k1, VerifyingKey, SigningKey

NODES = [
    'https://node.deso.org/api/v0/',
    'https://love4src.com/api/v0/',
]


def submitTransaction(signedTransactionHex, nodeURL=NODES[0]):
    endpointURL = nodeURL + "submit-transaction"
    payload = {"TransactionHex": signedTransactionHex}
    try:
        response = requests.post(endpointURL, json=payload)
    except requests.exceptions.Timeout:
        endpointURL = NODES[1] + "submit-transaction"
        response = requests.post(endpointURL, json=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response


def appendExtraData(
    transactionHex,
    derivedKey,
    nodeURL=NODES[0]
):

    payload = {
        "TransactionHex": transactionHex,
        "ExtraData": {"DerivedPublicKey": derivedKey},
    }
    endpointURL = nodeURL + "append-extra-data"

    try:
        response = requests.post(endpointURL, json=payload)
    except requests.exceptions.Timeout:
        endpointURL = NODES[1] + "append-extra-data"
        response = requests.post(endpointURL, json=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response


def validateJWT(JWT, publicKey):
    # this method is used to for public key validation
    try:
        rawPublicKeyHex = b58decode_check(publicKey)[3:].hex()
        public_key = bytes(rawPublicKeyHex, "utf-8")
        public_key = binascii.unhexlify(public_key)
        key = VerifyingKey.from_string(public_key, curve=SECP256k1)
        key = key.to_pem()
        decoded = jwt.decode(JWT, key, algorithms=["ES256"])
        return {"isValid": True, "decodedJWT": decoded}
    except Exception as e:
        return {"isValid": False, "error": str(e)}


def getUserJWT(seedHex):
    # returns JWT token of user that helps in public key validation in backend
    private_key = bytes(seedHex, "utf-8")
    private_key = binascii.unhexlify(private_key)
    key = SigningKey.from_string(private_key, curve=SECP256k1)
    key = key.to_pem()
    try:
        encoded_jwt = jwt.encode({}, key, algorithm="ES256")
    except jwt.InvalidIssuedAtError as e:
        return {"isValid": False, "error": str(e)}
    return encoded_jwt
