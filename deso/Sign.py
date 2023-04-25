# This file has code for signing a transaction --> Credit: MiniGlome and nathanwells
import hashlib
import hmac
import requests
from deso.Route import getRoute

def inverse_mod(k, p):
    """Returns the inverse of k modulo p.
    This function returns the only integer x such that (x * k) % p == 1.
    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError("division by zero")

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    return x % p


def get_hmac(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def hmac_drbg(entropy, string):
    material = entropy + string
    K = b"\x00" * 32
    V = b"\x01" * 32

    K = get_hmac(K, V + b"\x00" + material)
    V = get_hmac(K, V)
    K = get_hmac(K, V + b"\x01" + material)
    V = get_hmac(K, V)

    temp = b""
    while len(temp) < 32:
        V = get_hmac(K, V)
        temp += V

    return temp[:32]


#######


g = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def point_add(point1, point2):
    # Returns the result of point1 + point2 according to the group law.
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1) * inverse_mod(2 * y1, p)
    else:
        m = (y1 - y2) * inverse_mod(x1 - x2, p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % p, -y3 % p)

    return result


def scalar_mult(k, point):
    # Returns k * point computed using the double and point_add algorithm.
    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)
        # Double.
        addend = point_add(addend, addend)
        k >>= 1

    return result


#######


def to_DER(r, s):  # Signature to DER format
    r = bytes.fromhex(r)
    s = bytes.fromhex(s)
    if r[0] >= 0x80:
        r = bytes.fromhex("00") + r
    if s[0] >= 0x80:
        s = bytes.fromhex("00") + s
    res = (
        bytes.fromhex("02" + hex(len(r))[2:])
        + r
        + bytes.fromhex("02" + hex(len(s))[2:])
        + s
    )
    res = bytes.fromhex("30" + hex(len(res))[2:]) + res

    return res.hex()


def hexify(n):
    n = hex(n)[2:]
    if len(n) % 2 != 0:
        n = "0" + n
    return n
# New for the Balance Model fork
def getTransactionIndex(TransactionHex):
    endpointURL = getRoute() + "signature-index"
    payload = {"TransactionHex": TransactionHex}
    response = requests.post(endpointURL, json=payload)
    return response.json()['SignatureIndex']


def Sign_Transaction(seedHex, TransactionHex):
    transactionBytes = bytes.fromhex(TransactionHex)
    s256 = hashlib.sha256(
        hashlib.sha256(transactionBytes).digest()
    ).digest()
    drbg = hmac_drbg(entropy=bytes.fromhex(seedHex), string=s256)
    k = int.from_bytes(drbg, "big")
    kp = scalar_mult(k, g)
    kpX = kp[0]
    r = kpX % n
    s = inverse_mod(k, n) * (r * int(seedHex, 16) + int(s256.hex(), 16))
    s = s % n
    # Enforce low-s -> credit to @Nathanwells 
    if s > n // 2:
        s = n - s
    signature = to_DER(hexify(r), hexify(s))
    # Added for Balance Model fork
    signatureIndex = int(getTransactionIndex(TransactionHex))
    v0FieldsWithoutSignature = transactionBytes[:signatureIndex]
    v1FieldsBuffer = transactionBytes[1 + signatureIndex:]
    signed_transaction = (
        v0FieldsWithoutSignature.hex()
        + hex(len(bytearray.fromhex(signature)))[2:]
        + signature
        + v1FieldsBuffer.hex()
    )

    return signed_transaction
