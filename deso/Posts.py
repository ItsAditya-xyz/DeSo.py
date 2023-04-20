import requests


class Posts:
    def __init__(self, nodeURL="https://node.deso.org/api/v0/"):
        self.NODE_URL = nodeURL
        self.readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop",

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
        response = requests.post(endpointURL, json=payload)
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
            "FetchParents": fetchParents,
            "CommentOffset": commentOffset,
            "CommentLimit": commentLimit,
            "AddGlobalFeedBool": addGlobalFeedBool,
            "ThreadLevelLimit": ThreadLevelLimit,
            "ThreadLeafLimit": ThreadLeafLimit,
            "LoadAuthorThread": loadAuthorThread,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getPostsForPublicKey(
        self,
        username="",
        publicKey="",
        mediaRequired=False,
        numToFetch=10,
        lastPostHashHex="",
    ):
        endpoint = self.NODE_URL + "get-posts-for-public-key"
        payload = {
            "PublicKeyBase58Check": publicKey,
            "Username": username,
          
            "LastPostHashHex": lastPostHashHex,
            "NumToFetch": numToFetch,
            "MediaRequired": mediaRequired,
        }
        response = requests.post(endpoint, json=payload)
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
            
        }
        response = requests.post(endpointURL, json=payload)
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
 
        }
        response = requests.post(endpointURL, json=payload)
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
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getNFTEntriesForNFTPost(
        self,
        postHashHex,
    ):
        endpointURL = self.NODE_URL + "get-nft-entries-for-nft-post"
        payload = {
        
            "PostHashHex": postHashHex,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getNFTBidsForNFTPost(
        self,
        postHashHex,
    ):
        endpointURL = self.NODE_URL + "get-nft-bids-for-nft-post"
        payload = {
            "PostHashHex": postHashHex,
        }
        response = requests.post(endpointURL, json=payload)
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
           
            "SeenPosts": seenPosts,
            "Tag": f"{inputTag}",
            "SortByNew": sortByNew,
            "ResponseLimit": responseLimit,

        }
        response = requests.post(endpointURL, json=payload)
        return response
