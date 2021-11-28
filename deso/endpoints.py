class Route:
    API_BASE = "https://bitclout.com/api/v0/"

    def __init__(self, method, path):
        self.method = method
        self.path = path

    # Properties to get and set the API base
    @property
    def api_base(self):
        return self.API_BASE

    @api_base.setter
    def api_base(self, api_base):
        self.API_BASE = api_base

    # Returns the full path of the endpoint
    def full_path(self):
        return self.api_base + self.path


# Endpoints list
ENDPOINTS = {
    # Diamonds
    "diamonds": Route("GET", "get-diamonds-for-public-key"),
    # Messages
    "message": Route("POST", "send-message-stateless"),
    # Image
    "upload-image": Route("POST", "upload-image"),
    # Post
    "submit-post": Route("POST", "submit-post"),
    "get-posts-for-public-key": Route("POST", "get-posts-for-public-key"),
    "get-single-post": Route("POST", "get-single-post"),
    # NFT
    "create-nft": Route("POST", "create-nft"),
    "get-nft-entries": Route("POST", "get-nft-entries-for-nft-post"),
    "get-nfts-for-user": Route("POST", "get-nfts-for-user"),
    # Transaction
    "submit-transaction": Route("POST", "submit-transaction"),
    # Users
    "get-users-stateless": Route("POST", "get-users-stateless"),
    "get-single-profile": Route("POST", "get-single-profile"),
    "get-single-profiles": Route("POST", "get-single-profiles"),
    # Hodlers
    "get-hodlers-for-public-key": Route("POST", "get-hodlers-for-public-key"),
    # Notifs
    "get-notifications": Route("POST", "get-notifications"),
    # Creator coin
    "buy-or-sell-creator-coin": Route("POST", "buy-or-sell-creator-coin"),
}
