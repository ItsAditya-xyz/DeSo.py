import requests


NODES = [
    'https://node.deso.org/api/v0/',
    'https://love4src.com/api/v0/',
]

class Posts:
    def __init__(self,
            nodeURL=NODES[0],
            readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop"
            ):
        self.NODE_URL = nodeURL
        self.readerPublicKey = readerPublicKey

    def getPostsStateless(
        self,
        addGlobalFeedBool=False,
        fetchSubcommnets=False,
        getPostsByDESO=False,
        getPostsForFollowFeed=False,
        getPostsForGlobalWhitelist=True,
        mediaRequired=False,
        numToFetch=50,
        orderBy="",
        postContent="",
        postHashHex="",
        postsByDESOMinutesLookBack=0,
        customPayload={},
    ):
        endpointURL = self.NODE_URL + "get-posts-stateless"
        payload = {
            "PostHashHex": postHashHex,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "OrderBy": orderBy,
            "StartTstampSecs": None,
            "PostContent": postContent,
            "NumToFetch": numToFetch,
            "FetchSubcomments": fetchSubcommnets,
            "GetPostsForFollowFeed": getPostsForFollowFeed,
            "GetPostsForGlobalWhitelist": getPostsForGlobalWhitelist,
            "GetPostsByDESO": getPostsByDESO,
            "MediaRequired": mediaRequired,
            "PostsByDESOMinutesLookback": postsByDESOMinutesLookBack,
            "AddGlobalFeedBool": addGlobalFeedBool,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)
        return response

    def getSinglePost(
        self,
        postHashHex,
        fetchParents=False,
        commentLimit=10,
        commentOffset=0,
        addGlobalFeedBool=False,
        loadAuthorThread=True,
        ThreadLeafLimit=1,
        ThreadLevelLimit=2,
    ):
        endpointURL = self.NODE_URL + "get-single-post"
        payload = {
            "PostHashHex": postHashHex,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "FetchParents": fetchParents,
            "CommentOffset": commentOffset,
            "CommentLimit": commentLimit,
            "AddGlobalFeedBool": addGlobalFeedBool,
            "ThreadLevelLimit": ThreadLevelLimit,
            "ThreadLeafLimit": ThreadLeafLimit,
            "LoadAuthorThread": loadAuthorThread,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)
        return response

    def getPostsForPublicKey(
        self,
        username="",
        publicKey="",
        mediaRequired=False,
        numToFetch=10,
        lastPostHashHex="",
    ):
        endpointURL = self.NODE_URL + "get-posts-for-public-key"
        payload = {
            "PublicKeyBase58Check": publicKey,
            "Username": username,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "LastPostHashHex": lastPostHashHex,
            "NumToFetch": numToFetch,
            "MediaRequired": mediaRequired,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getDiamondsForPost(
        self,
        postHashHex,
        limit=25,
        offset=0,
    ):
        endpointURL = self.NODE_URL + "get-diamonds-for-post"
        payload = {
            "PostHashHex": postHashHex,
            "Offset": offset,
            "Limit": limit,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getLikesForPost(
        self,
        postHashHex,
        limit=50,
        offset=0,
    ):
        endpointURL = self.NODE_URL + "get-likes-for-post"
        payload = {
            "PostHashHex": postHashHex,
            "Offset": offset,
            "Limit": limit,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getQuoteRepostsForPost(
        self,
        postHashHex,
        limit=50,
        offset=0,
    ):
        endpointURL = self.NODE_URL + "get-quote-reposts-for-post"
        payload = {
            "PostHashHex": postHashHex,
            "Offset": offset,
            "Limit": limit,
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getNFTEntriesForNFTPost(
        self,
        postHashHex,
    ):
        endpointURL = self.NODE_URL + "get-nft-entries-for-nft-post"
        payload = {
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "PostHashHex": postHashHex,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getNFTBidsForNFTPost(
        self,
        postHashHex,
    ):
        endpointURL = self.NODE_URL + "get-nft-bids-for-nft-post"
        payload = {
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "PostHashHex": postHashHex,
        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response

    def getHotFeed(
        self,
        taggedUsername = "",
        responseLimit=10,
        sortByNew=True,
        seenPosts=[],
        hashtag = ""
    ):
        if taggedUsername:
            inputTag = "@" +   taggedUsername
        elif hashtag:
            inputTag = "#" +   hashtag
        else:
            inputTag=""
        """Returns posts that has mentioned in username"""
        endpointURL = self.NODE_URL + "get-hot-feed"
        payload = {
            "ReaderPublicKeyBase58Check": self.readerPublicKey,
            "SeenPosts": seenPosts,
            "Tag": f"{inputTag}",
            "SortByNew": sortByNew,
            "ResponseLimit": responseLimit,

        }
        try:
            response = requests.post(endpointURL, json=payload)
        except requests.exceptions.RequestException as e:
            self.NODE_URL = NODES[1]
            response = requests.post(endpointURL, json=payload)
        except:
            raise SystemExit(e)

        return response
