import sys

import requests

from .endpoints import Route


class BaseClient:
    def __init__(self, public_key, seed_hex) -> None:
        self.public_key = public_key
        self.seed_hex = seed_hex

        # Get the __version__ from the package
        from deso import __version__

        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # Assign headers
        self.headers = {
            "User-Agent": f"Deso.py[v{__version__}] Client (https://github.com/AdityaChaudhary0005/DeSo.py) "
            f"Python/{python_version}"
        }

    # Define the fetch method
    def fetch_api(self, route: Route, headers: dict = None, body: dict = None, files=None, text: bool = False) -> dict:
        # If headers are provided, add them
        if headers:
            self.headers.update(headers)

        # If the route is not GET, ensure body exists
        if route.method != "GET" and not body:
            raise ValueError("Body must be provided for non-GET requests")

        # Core fetch logic
        with requests.request(
            route.method, route.full_path(), headers=self.headers, data=body, files=files,
        ) as response:
            # Handle errors separately
            if response.status_code == 404:
                raise ValueError("404, Not Found")

            # 429
            if response.status_code == 429:
                raise ValueError("429, Too Many Requests")

            # 500
            if response.status_code == 500:
                raise ValueError("500, Internal Server Error")

            # Invalid method
            if response.status_code == 405:
                raise ValueError("405, Method Not Allowed")

            # Return the response JSON
            if text:
                return response.status_code, response.text

            return response.status_code, response.json()
