# This file has code for signing a transaction --> Credit: MiniGlome
import hashlib
import hmac


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


g = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
     0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


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
        m = (3 * x1 * x1) * pow(2 * y1, -1, p)
    else:
        m = (y1 - y2) * pow(x1 - x2, -1, p)

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
        r = bytes.fromhex("00")+r
    if s[0] >= 0x80:
        s = bytes.fromhex("00")+s
    res = bytes.fromhex("02"+hex(len(r))[2:]) + \
        r + bytes.fromhex("02"+hex(len(s))[2:]) + s
    res = bytes.fromhex("30"+hex(len(res))[2:]) + res

    return res.hex()


def hexify(n):
    n = hex(n)[2:]
    if len(n) % 2 != 0:
        n = "0"+n
    return n


def Sign_Transaction(seedHex, TransactionHex):
    s256 = hashlib.sha256(hashlib.sha256(
        bytes.fromhex(TransactionHex)).digest()).digest()
    drbg = hmac_drbg(entropy=bytes.fromhex(seedHex), string=s256)
    k = int.from_bytes(drbg, 'big')
    kp = scalar_mult(k, g)
    kpX = kp[0]
    r = kpX % n
    s = pow(k, -1, n) * (r * int(seedHex, 16)+int(s256.hex(), 16))
    s = s % n
    signature = to_DER(hexify(r), hexify(s))
    signed_transaction = TransactionHex[:-2] + \
        hex(len(bytearray.fromhex(signature)))[2:] + signature

    return signed_transaction
