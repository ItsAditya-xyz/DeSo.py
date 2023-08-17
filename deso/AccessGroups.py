from deso.utils import submitTransaction, appendExtraData
import requests
from deso.Sign import Sign_Transaction


class AccessGroups:
    def __init__(self,
                 publicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop",
                 nodeURL="https://node.deso.org/api/v0/",
                 readerPublicKey="BC1YLgk64us61PUyJ7iTEkV4y2GqpHSi8ejWJRnZwsX6XRTZSfUKsop",
                 seedHex=None,
                 derivedPublicKey=None,
                 derivedSeedHex=None,
                 minFee=1000,
                 derivedKeyFee=1700,
                 appName="DesoPy",
                 ):
        self.SEED_HEX = seedHex
        self.PUBLIC_KEY = publicKey
        self.NODE_URL = nodeURL
        self.appName = appName
        self.DERIVED_PUBLIC_KEY = derivedPublicKey
        self.DERIVED_SEED_HEX = derivedSeedHex
        self.MIN_FEE = minFee if seedHex else derivedKeyFee
        self.READER_PUBLIC_KEY = readerPublicKey

    def getAllAccessGroups(self, publicKey):
        endpointURL = self.NODE_URL + "get-all-user-access-groups"
        payload = {
            "PublicKeyBase58Check": publicKey,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getAllOwnedAccessGroups(self, publicKey):
        endpointURL = self.NODE_URL + "get-all-user-access-groups-owned"
        payload = {
            "PublicKeyBase58Check": publicKey,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getAllUserAccessGroupMembersOnly(self, publicKey):
        endpointURL = self.NODE_URL + "get-all-user-access-groups-member-only"
        payload = {
            "PublicKeyBase58Check": publicKey,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def checkPartlyAccessGroups(self,  senderGroupAccessKeyName, senderPublicKey,  recipientAccessGroupKeyName, recipientPublicKey):
        '''Check Party Access Groups checks whether both the sender and receiver have the requested access groups. 
        If they do not, it returns the base key.'''
        endpointURL = self.NODE_URL + "check-party-access-groups"
        payload = {
            "SenderPublicKeyBase58Check": senderPublicKey,
            "SenderAccessGroupKeyName": senderGroupAccessKeyName,
            "RecipientPublicBase58Check": receiverPublicKey,
            "RecipientAccessGroupKeyName": receiverGroupAccessKeyName,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getAccessGroupInfo(self, accessGroupKeyName, accessGroupOwnerPublicKey):
        '''gets a single Access Group Member Entry Response for the access group member defined in the request body.'''
        endpointURL = self.NODE_URL + "get-access-group-info"
        payload = {
            "AccessGroupOwnerPublicKeyBase58Check": accessGroupOwnerPublicKey,
            "AccessGroupKeyName": accessGroupKeyName,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getAccessGroupMemberInfo(self, accessGroupKeyName, accessGroupOwnerPublicKey, accessGroupMemberPublicKey):
        '''gets a single Access Group Member Entry Response for the access group member defined in the request body.'''
        endpointURL = self.NODE_URL + "get-access-group-member-info" 
        payload = {
            "AccessGroupOwnerPublicKeyBase58Check": accessGroupOwnerPublicKey,
            "AccessGroupKeyName": accessGroupKeyName,
            "AccessGroupMemberPublicKeyBase58Check": accessGroupMemberPublicKey,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getPaginatedAccessGroupMembers(self, accessGroupKeyName, accessGroupOwnerPublicKey, startingAccessGroupMemberPublicKey, numToFetch):
        '''gets a page of Access Group Member Entry responses for the access group defined in the request body. 
        This is useful in identifying all members of a group. A map of public key to profile entry response is provided for convenience.'''
        endpointURL = self.NODE_URL + "get-paginated-access-group-members"
        payload = {
            "AccessGroupOwnerPublicKeyBase58Check": accessGroupOwnerPublicKey,
            "AccessGroupKeyName": accessGroupKeyName,
            "StartingAccessGroupMemberPublicKeyBase58Check": startingAccessGroupMemberPublicKey,
            "MaxMembersToFetch": numToFetch,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getBulkAccessGroupEntries(self, groupOwnerAndGroupKeyNameList):
        # takes an array of objects having 'accessGroupKeyName' and 'accessGroupOwnerPublicKey' fields and returns info in bulk
        endpointURL = self.NODE_URL + "get-bulk-access-group-entries"
        payload = {
            "GroupOwnerAndGroupKeyNamePairs": groupOwnerAndGroupKeyNameList
        }
        response = requests.post(endpointURL, json=payload)
        return response