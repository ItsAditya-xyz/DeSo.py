from deso.utils import getUserJWT
import requests

NODES = [
    'https://node.deso.org/api/v0/',
    'https://love4src.com/api/v0/',
]


class Media:
    def __init__(
        self,
        publicKey=None,
        seedHex=None,
        nodeURL=NODES[0],
    ):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL

    def uploadImage(self, fileList):
        # uploads image to images.deso.org

        if isinstance(fileList, str):
            try:
                fileList = [
                    ("file", (fileList, open(fileList, "rb"), "image/png"))
                ]
            except OSError:
                raise SystemExit("File not found")

        jwt_token = getUserJWT(self.SEED_HEX)
        # print(encoded_jwt)
        endpointURL = self.NODE_URL + "upload-image"
        payload = {
            "UserPublicKeyBase58Check": self.PUBLIC_KEY,
            "JWT": jwt_token,
        }
        try:
            response = requests.post(endpointURL,
                                     data=payload,
                                     files=fileList)
        except requests.exceptions.Timeout:
            endpointURL = NODES[1] + "get-single-profile"
            response = requests.post(endpointURL,
                                     data=payload,
                                     files=fileList)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response
