import requests


class Posts:
    def __init__(self,  nodeURL="https://node.deso.org/api/v0/"):
        self.NODE_URL = nodeURL

    def getPostsStateless(self, readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop", addGlobalFeedBool=False, fetchSubcommnets=False, getPostsByDESO=False, getPostsForFollowFeed=False, getPostsForGlobalWhitelist=True, mediaRequired=False, numToFetch=50, orderBy="", postContent="", postHashHex="", postsByDESOMinutesLookBack=0, customPayload={}):
        endpointURL = self.NODE_URL + "get-posts-stateless"
        payload = {"PostHashHex": postHashHex,
                   "ReaderPublicKeyBase58Check": readerPublicKey,
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
                   "AddGlobalFeedBool": addGlobalFeedBool}
        response = requests.post(endpointURL, json=payload)
        return response

    def getSinglePost(self, postHashHex, readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop", fetchParents=False, commnetLimit=10, commentOffset=0, addGlobalFeedBool=False, loadAuthorThread=True, ThreadLeafLimit=1, ThreadLevelLimit=2):
        endpointURL = self.NODE_URL + "get-single-post"
        payload = {"PostHashHex": postHashHex,
                   "ReaderPublicKeyBase58Check": readerPublicKey,
                   "FetchParents": fetchParents,
                   "CommentOffset": commentOffset,
                   "CommentLimit": commnetLimit,
                   "AddGlobalFeedBool": addGlobalFeedBool,
                   "ThreadLevelLimit": ThreadLevelLimit,
                   "ThreadLeafLimit": ThreadLeafLimit,
                   "LoadAuthorThread": loadAuthorThread}
        response = requests.post(endpointURL, json=payload)
        return response

    def getPostsForPublicKey(self, username="", publicKey="", mediaRequired=False, numToFetch=10, lastPostHashHex="", readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop"):
        endpoint = self.NODE_URL + "get-posts-for-public-key"
        payload = {"PublicKeyBase58Check": publicKey,
                   "Username": username,
                   "ReaderPublicKeyBase58Check": readerPublicKey,
                   "LastPostHashHex": lastPostHashHex,
                   "NumToFetch": numToFetch,
                   "MediaRequired": mediaRequired}
        response = requests.post(endpoint, json=payload)
        return response

    def getDiamondsForPost(self, postHashHex, limit=25, offset=0, readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop"):
        endpointURL = self.NODE_URL + "get-diamonds-for-post"
        payload = {"PostHashHex": postHashHex,
                   "Offset": offset,
                   "Limit": limit,
                   "ReaderPublicKeyBase58Check": readerPublicKey}
        response = requests.post(endpointURL, json=payload)
        return response

    def getLikesForPost(self, postHashHex, limit=50, offset=0, readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop"):
        endpointURL = self.NODE_URL + "get-likes-for-post"
        payload = {"PostHashHex": postHashHex,
                   "Offset": offset,
                   "Limit": limit,
                   "ReaderPublicKeyBase58Check": readerPublicKey}
        response = requests.post(endpointURL, json=payload)
        return response

    def getQuoteRepostsForPost(self, postHashHex, limit=50, offset=0, readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop"):
        endpointURL = self.NODE_URL + "get-quote-reposts-for-post"
        payload = {"PostHashHex": postHashHex,
                   "Offset": offset,
                   "Limit": limit,
                   "ReaderPublicKeyBase58Check": readerPublicKey}
        response = requests.post(endpointURL, json=payload)
        return response
