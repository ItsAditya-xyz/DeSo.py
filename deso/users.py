from .base import BaseClient
from .endpoints import ENDPOINTS, Route


class Users(BaseClient):
    def __init__(self, public_key, seed_hex) -> None:
        super().__init__(public_key, seed_hex)

    @staticmethod
    def get_profile_picture(public_key):
        return (
            f"https://bitclout.com/api/v0/get-single-profile-picture/{public_key}?"
            f"fallback=https://bitclout.com/assets/img/default_profile_pic.png"
        )

    def get_user_stateless(self, public_key_list, skip_for_leaderboard=True):
        payload = {
            "PublicKeysBase58Check": public_key_list,
            "SkipForLeaderboard": skip_for_leaderboard,
        }

        route = ENDPOINTS["get-users-stateless"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_profile(self, public_key, username):
        payload = {"PublicKeyBase58Check": public_key, "Username": username}

        route = ENDPOINTS["get-single-profile"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_users_blocked(self, public_key):
        payload = {"PublicKeysBase58Check": [public_key], "SkipForLeaderboard": False}

        route = ENDPOINTS["get-users-stateless"]
        _, json = self.fetch_api(route, body=payload)

        return json["UserList"][0]["BlockedPubKeys"]

    def get_username_from_key(self, public_key):
        payload = {"PublicKeyBase58Check": public_key, "Username": ""}

        route = ENDPOINTS["get-single-profiles"]
        _, json = self.fetch_api(route, body=payload)

        try:
            return json["Profile"]["Username"]
        except Exception:
            return public_key

    def get_notifications(self, public_key, start_index=-1, num_to_fetch=50):
        payload = {
            "PublicKeyBase58Check": public_key,
            "FetchStartIndex": start_index,
            "NumToFetch": num_to_fetch,
        }

        route = ENDPOINTS["get-notifications"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_wallet(self, public_key, include_creator_coin=True):
        payload = {
            "PublicKeysBase58Check": [public_key],
            "SkipForLeaderboard": False,
        }

        # Route
        route = ENDPOINTS["get-users-stateless"]

        # Fetch
        response = self.fetch_api(route, body=payload)
        final_resp = {}

        if include_creator_coin:
            coin_held = response["UserList"][0]["UsersYouHODL"]
            final_resp["CoinsHeldInfo"] = coin_held

        clout_in_wallet = response["UserList"][0]["BalanceNanos"]
        final_resp["CloutInWalletNanos"] = clout_in_wallet

        return final_resp

    def get_hodlers(
        self,
        username="",
        public_key="",
        last_public_key="",
        num_to_fetch=100,
        fetch_all=False,
    ):
        payload = {
            "PublicKeyBase58Check": public_key,
            "Username": username,
            "LastPublicKeyBase58Check": last_public_key,
            "NumToFetch": num_to_fetch,
            "FetchHodlings": False,
            "FetchAll": fetch_all,
        }

        # Route and fetch
        route = ENDPOINTS["get-hodlers-for-public-key"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_nfts(self, user_public_key, reader_public_key="", is_for_sale=False):
        payload = {
            "UserPublicKeyBase58Check": user_public_key,
            "ReaderPublicKeyBase58Check": reader_public_key,
            "IsForSale": is_for_sale,
        }

        # Route and fetch
        route = ENDPOINTS["get-nfts-for-user"]
        _, json = self.fetch_api(route, body=payload)

        return json

    def get_transaction_info(
        self,
        public_key,
        limit=200,
        last_transaction_id_base58_check="",
        last_public_key_transaction_idx=-1,
    ):
        # Payload
        payload = {
            "PublicKeyBase58Check": public_key,
            "LastTransactionIDBase58Check": last_transaction_id_base58_check,
            "LastPublicKeyTransactionIndex": last_public_key_transaction_idx,
            "Limit": limit,
        }

        # Create route
        route = Route("POST", "transaction-info")
        route.API_BASE = "https://api.bitclout.com/api/v1/"

        # Fetch
        _, json = self.fetch_api(route, body=payload)
        return json
