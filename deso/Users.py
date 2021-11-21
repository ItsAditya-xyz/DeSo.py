import requests
import json
from deso.Route import getRoute


class Users:
    def getUserStateless(publicKeyList, skipForLeaderboard=True):
        '''when skipForLeaderboard is true, it doesn't return info like UsersYouHODL,
            followers public key and blocked users'''
        payload = {"PublicKeysBase58Check": publicKeyList,
                   "SkipForLeaderboard": skipForLeaderboard}
        route = getRoute()
        endpointURL = route + "get-users-stateless"
        response = requests.post(endpointURL, json=payload)
        return response.json()

    def getSingleProfile(publicKey="", username="",):
        payload = {"PublicKeyBase58Check": publicKey, "Username": username}
        route = getRoute()
        endpointURL = route + "get-single-profile"
        response = requests.post(endpointURL, json=payload)
        return response.json()

    def getProfilePic(publicKey):
        profilePicURL = f'https://bitclout.com/api/v0/get-single-profile-picture/{publicKey}?fallback=https://bitclout.com/assets/img/default_profile_pic.png'
        return profilePicURL

    def getUsersBlocked(publicKey):
        payload = {"PublicKeysBase58Check": [
            publicKey], "SkipForLeaderboard": False}
        route = getRoute()
        endpointURL = route + "get-users-stateless"
        response = requests.post(endpointURL, json=payload)
        return response.json()["UserList"][0]["BlockedPubKeys"]

    def getUsernameFromKey(publicKey):
        route = getRoute()
        endpointURL = route + "get-single-profiles"
        payload = {"PublicKeyBase58Check": publicKey, "Username": ""}
        response = requests.post(url=endpointURL, json=payload)

        try:
            return response.json()["Profile"]["Username"]
        except Exception as e:
            return publicKey

    def getWallet(publicKey, includeCreatorCoin=True):
        # returns $DESO in wallet and Creators coins on whom the user has invested in
        try:
            payload = {"PublicKeysBase58Check": [
                publicKey], "SkipForLeaderboard": False}
            route = getRoute()
            endpointURL = route + "get-users-stateless"
            response = requests.post(endpointURL, json=payload)
            responseJson = response.json()
            finalResponse = {
            }
            if includeCreatorCoin:
                coinHeld = responseJson["UserList"][0]["UsersYouHODL"]
                finalResponse["CoinsHeldInfo"] = coinHeld

            CloutInWallet = responseJson["UserList"][0]["BalanceNanos"]
            finalResponse["CloutInWalletNanos"] = CloutInWallet
            return finalResponse
        except Exception as e:
            return response.status_code

    def getHodlers(username="", publicKey="", lastPublicKey="", numToFetch=100, fetchAll=False):
        payload = {"PublicKeyBase58Check": publicKey,
                   "Username": username,
                   "LastPublicKeyBase58Check": lastPublicKey,
                   "NumToFetch": numToFetch,
                   "FetchHodlings": False,
                   "FetchAll": fetchAll}
        route = getRoute()
        endpointURL = route + "get-hodlers-for-public-key"
        response = requests.post(endpointURL, json=payload)
        return response.json()

    def getTransactionInfo(publicKey, limit=200, lastTransactionIDBase58Check="", lastPublicKeyTransactionIndex=-1):
        payload = {"PublicKeyBase58Check": publicKey,
                   "LastTransactionIDBase58Check": lastTransactionIDBase58Check,
                 "LastPublicKeyTransactionIndex": lastPublicKeyTransactionIndex, "Limit": limit}
        endpointURL = "https://api.bitclout.com/api/v1/transaction-info"
        response = requests.post(endpointURL, json=payload)
        return response.json()


    def getNotifications(publicKey, startIndex = -1, numToFetch = 50):
        payload = {"PublicKeyBase58Check": publicKey,
                   "FetchStartIndex": startIndex,
                   "NumToFetch": numToFetch}
        route = getRoute()
        endpointURL = route + "get-notifications"
        response = requests.post(endpointURL, json=payload)
        return response.json()