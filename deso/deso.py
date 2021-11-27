from .base import BaseClient
from .endpoints import Route


class Deso(BaseClient):
    def __init__(self, public_key, *args, **kwargs) -> None:
        super().__init__(public_key, *args, **kwargs)

    def get_deso_price(self) -> dict:
        route = Route("GET", "https://api.blockchain.com/v3/exchange/tickers/CLOUT-USD")
        return self.fetch_api(route)
