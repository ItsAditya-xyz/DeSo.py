from .base import BaseClient
from .endpoints import ENDPOINTS


class Diamonds(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def get_diamonds(self, received=True):
        # Route
        route = ENDPOINTS["diamonds"]

        # Payload
        payload = {
            "PublicKeyBase58Check": self.public_key,
            "FetchYouDiamonded": not received,
        }

        # Fetch and return
        _, json = self.fetch_api(route, payload)

        return json
