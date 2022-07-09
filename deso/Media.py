from deso.utils import getUserJWT
import requests


class Media:
    def __init__(
        self,
        publicKey=None,
        seedHex=None,
        nodeURL="https://node.deso.org/api/v0/",
    ):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL

    def uploadImage(self, fileList):
        # uploads image to images.deso.org
        try:
            if type(fileList) == type("str"):
                fileList = [
                    ("file", (fileList, open(fileList, "rb"), "image/png"))
                ]

            jwt_token = getUserJWT(self.SEED_HEX)
            # print(encoded_jwt)
            endpointURL = self.NODE_URL + "upload-image"
            payload = {
                "UserPublicKeyBase58Check": self.PUBLIC_KEY,
                "JWT": jwt_token,
            }

            response = requests.post(endpointURL, data=payload, files=fileList)
            return response
        except Exception as e:
            return e
