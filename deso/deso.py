from .base import BaseClient
from .endpoints import Route


class Deso(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def get_deso_price(self) -> dict:
        route = Route("GET", "https://api.blockchain.com/v3/exchange/tickers/CLOUT-USD")
        _, json = self.fetch_api(route)
        return json
