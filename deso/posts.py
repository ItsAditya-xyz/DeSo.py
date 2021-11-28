import requests

from .base import BaseClient
from .endpoints import ENDPOINTS


class Posts(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    def get_user_posts(
            self,
            username="",
            public_key="",
            num_to_fetch=10,
            media_required=False,
            last_post_hash="",
            reader_public_key="BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB",
    ):
        payload = {
            "PublicKeyBase58Check": public_key,
            "Username": username,
            "ReaderPublicKeyBase58Check": reader_public_key,
            "LastPostHashHex": last_post_hash,
            "NumToFetch": num_to_fetch,
            "MediaRequired": media_required,
        }

        # Route
        route = ENDPOINTS["get-posts-for-public-key"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_post_info(
            self,
            post_hash,
            comment_limit=20,
            fetch_parents=False,
            comment_offset=0,
            add_global_feed_bool=False,
            reader_public_key="BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB",
    ):
        payload = {
            "PostHashHex": post_hash,
            "ReaderPublicKeyBase58Check": reader_public_key,
            "FetchParents": fetch_parents,
            "CommentOffset": comment_offset,
            "CommentLimit": comment_limit,
            "AddGlobalFeedBool": add_global_feed_bool,
        }

        # Route and request
        route = ENDPOINTS["get-single-post"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_hidden_posts(self, public_key):
        payload = {
            "userParams": {
                "queryParams": {"length": 0},
                "headersParams": {"length": 0},
                "cookiesParams": {"length": 0},
                "bodyParams": {"0": public_key, "length": 1},
            },
            "password": "",
            "environment": "production",
            "queryType": "RESTQuery",
            "frontendVersion": "1",
            "releaseVersion": None,
            "includeQueryExecutionMetadata": True,
        }

        # Make request
        response = requests.post(
            "https://apps.tryretool.com/api/public/8952bb20-817f-46f0-b28f-67569f4db682/query?queryName=getHiddenPosts",
            json=payload,
        )
        return response.json()
