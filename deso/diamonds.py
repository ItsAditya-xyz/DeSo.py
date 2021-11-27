from .base import BaseClient
from .endpoints import ENDPOINTS


class Diamonds(BaseClient):
    def __init__(self, public_key, *args, **kwargs) -> None:
        super().__init__(public_key, *args, **kwargs)

    def get_diamonds(self, received=True):
        # Route
        route = ENDPOINTS["diamonds"]

        # Payload
        payload = {
            "PublicKeyBase58Check": self.public_key,
            "FetchYouDiamonded": not received,
        }

        # Fetch and return
        return self.fetch_api(route, payload)
