from deso.utils import submitTransaction, appendExtraData
import requests
from deso.Sign import Sign_Transaction


class Associations:
    def __init__(self, 
        publicKey="BC1YLhfrQMbHHZVw6XH38eHtYJaQtk4hYoKDy3mKmd88b141hZYcGGM",
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


    def getUserAssociationById(self, association_id):
        endpointURL = self.NODE_URL + "user-associations/" + association_id
        
        response = requests.get(endpointURL)
        return response
    
    def createUserAssociation(self, 
                              transactorKey, 
                              targetUserKey, 
                              associationType, 
                              associationValue,
                              appKey=None,
                              postExtraData={"Language": "en"},
                              ):
        
        postExtraData["App"] = self.appName

        try:
            error = None
            endpointURL = self.NODE_URL + "user-associations/create"
            finalPostExtraData = postExtraData
            if (
                self.DERIVED_PUBLIC_KEY is not None
                and self.DERIVED_SEED_HEX is not None
                and self.SEED_HEX is None
            ):
                if "DerivedPublicKey" not in finalPostExtraData:
                    finalPostExtraData[
                        "DerivedPublicKey"
                    ] = self.DERIVED_PUBLIC_KEY

        
            payload = {
                "TransactorPublicKeyBase58Check": transactorKey,
                "TargetUserPublicKeyBase58Check": targetUserKey,
                "AppPublicKeyBase58Check": appKey,
                "AssociationType": associationType,
                "AssociationValue": associationValue,
                "ExtraData": finalPostExtraData,
                "MinFeeRateNanosPerKB": self.MIN_FEE,
            }
            response = requests.post(endpointURL, json=payload)
            transactionHex = response.json()["TransactionHex"]
            seedHexToSignWith = (
                self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            )
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex
                )
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL
            )
            
            return submitTransactionResponse
        
        except Exception as e:
            error = {
                    "error": "Something went wrong while signing the transactions."
                }

    def deleteUserAssociation(self, 
                              transactorKey,
                              association_id,
                              postExtraData={"Language": "en"},
                              ):
        
        postExtraData["App"] = self.appName

        try:
            error = None
            endpointURL = self.NODE_URL + "user-associations/delete"
            finalPostExtraData = postExtraData
            if (
                self.DERIVED_PUBLIC_KEY is not None
                and self.DERIVED_SEED_HEX is not None
                and self.SEED_HEX is None
            ):
                if "DerivedPublicKey" not in finalPostExtraData:
                    finalPostExtraData[
                        "DerivedPublicKey"
                    ] = self.DERIVED_PUBLIC_KEY

            payload = {
                "TransactorPublicKeyBase58Check": transactorKey,
                "AssociationID": association_id,
                "ExtraData": finalPostExtraData,
                "MinFeeRateNanosPerKB": self.MIN_FEE,
            }
            response = requests.post(endpointURL, json=payload)
            print(response.json(), 'first response')
            transactionHex = response.json()["TransactionHex"]
            seedHexToSignWith = (
                self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            )
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex
                )
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL
            )
            print(submitTransactionResponse.json(), 'second response')
            
            return submitTransactionResponse




        except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }

    def countUserAssociations(self, transactorKey=None, targetUserKey=None, appKey=None, associationType=None, associationTypePrefix=None, value=None, valuePrefix=None, ):
        endpointURL = self.NODE_URL + "user-associations/count"
        payload = {
            "TransactorPublicKeyBase58Check": transactorKey,
            "TargetUserPublicKeyBase58Check": targetUserKey,
            "AppPublicKeyBase58Check": appKey,
            "AssociationType": associationType,
            "AssociationTypePrefix": associationTypePrefix,
            "AssociationValue": value,
            "AssociationValuePrefix": valuePrefix,
        }
        response = requests.post(endpointURL, json=payload)
        return response
    
    def countUserAssociationsByMultipleValues(self, transactorKey=None, targetUserKey=None, appKey=None, associationType="", associationValues=[]):
        endpointURL = self.NODE_URL + "user-associations/counts"
        payload = {
            "TransactorPublicKeyBase58Check": transactorKey,
            "TargetUserPublicKeyBase58Check": targetUserKey,
            "AppPublicKeyBase58Check": appKey,
            "AssociationType": associationType,
            "AssociationValues": associationValues,
        }
        response = requests.post(endpointURL, json=payload)
        return response
    
    def queryForUserAssociations(self, transactorKey=None, targetUserKey=None, appKey=None, associationType=None, associationTypePrefix=None, value=None, valuePrefix=None, associationValues=[],
                                 limit=100, lastSeenAssociationID=None, sortDescending=False, includeTransactorProfile=False, includeTargetUserProfile=False, includeAppProfile=False, 
                                 ):
        endpointURL = self.NODE_URL + "user-associations/query"
        payload = {
            "TransactorPublicKeyBase58Check": transactorKey,
            "TargetUserPublicKeyBase58Check": targetUserKey,
            "AppPublicKeyBase58Check": appKey,
            "AssociationType": associationType,
            "AssociationTypePrefix": associationTypePrefix,
            "AssociationValue": value,
            "AssociationValuePrefix": valuePrefix,
            "AssociationValues": associationValues,
            "Limit": limit,
            "LastSeenAssociationID": lastSeenAssociationID,
            "SortDescending": sortDescending,
            "IncludeTransactorProfile": includeTransactorProfile,
            "IncludeTargetUserProfile": includeTargetUserProfile,
            "IncludeAppProfile": includeAppProfile,
        }
        response = requests.post(endpointURL, json=payload)
        return response

    def getPostAssociationsByID(self, association_id):
        endpointURL = self.NODE_URL + "post-associations/" + association_id        
        response = requests.get(endpointURL)
        return response
    
    def countPostAssociations(self, transactorKey=None, postHashHex=None, appKey=None, associationType=None, associationTypePrefix=None, value=None, valuePrefix=None, ):
        endpointURL = self.NODE_URL + "post-associations/count"
        payload = {
            "TransactorPublicKeyBase58Check": transactorKey,
            "PostHashHex": postHashHex,
            "AppPublicKeyBase58Check": appKey,
            "AssociationType": associationType,
            "AssociationTypePrefix": associationTypePrefix,
            "AssociationValue": value,
            "AssociationValuePrefix": valuePrefix,
        }
        response = requests.post(endpointURL, json=payload)
        return response
        
    def countPostAssociationsByMultipleValues(self, transactorKey=None, postHashHex=None, appKey=None, associationType="", associationValues=[]):
        endpointURL = self.NODE_URL + "post-associations/counts"
        payload = {
            "TransactorPublicKeyBase58Check": transactorKey,
            "PostHashHex": postHashHex,
            "AppPublicKeyBase58Check": appKey,
            "AssociationType": associationType,
            "AssociationValues": associationValues,
        }
        response = requests.post(endpointURL, json=payload)
        return response
    
    def queryForPostAssociations(self, transactorKey=None, postHashHex=None, appKey=None, associationType=None, associationTypePrefix=None, value=None, valuePrefix=None, associationValues=[],
                                    limit=100, lastSeenAssociationID=None, sortDescending=False, includeTransactorProfile=False, includePostEntry=False, includePostAuthorProfile=False, includeAppProfile=False,
                                    ):
            endpointURL = self.NODE_URL + "post-associations/query"
            payload = {
                "TransactorPublicKeyBase58Check": transactorKey,
                "PostHashHex": postHashHex,
                "AppPublicKeyBase58Check": appKey,
                "AssociationType": associationType,
                "AssociationTypePrefix": associationTypePrefix,
                "AssociationValue": value,
                "AssociationValuePrefix": valuePrefix,
                "AssociationValues": associationValues,
                "Limit": limit,
                "LastSeenAssociationID": lastSeenAssociationID,
                "SortDescending": sortDescending,
                "IncludeTransactorProfile": includeTransactorProfile,
                "IncludePost": includePostEntry,
                "IncludePostAuthorProfile": includePostAuthorProfile,
                "IncludeAppProfile": includeAppProfile,
            }
            response = requests.post(endpointURL, json=payload)
            return response
    
    def createPostAssociation(self, transactorKey, postHashHex, associationType, associationValue, appKey=None, postExtraData={"Language": "en"}, ):
        
        postExtraData["App"] = self.appName

        try:
            error = None
            endpointURL = self.NODE_URL + "post-associations/create"
            finalPostExtraData = postExtraData
            
            if (
                self.DERIVED_PUBLIC_KEY is not None
                and self.DERIVED_SEED_HEX is not None
                and self.SEED_HEX is None
            ):
                if "DerivedPublicKey" not in finalPostExtraData:
                    finalPostExtraData[
                        "DerivedPublicKey"
                    ] = self.DERIVED_PUBLIC_KEY

            payload = {
                "TransactorPublicKeyBase58Check": transactorKey,
                "PostHashHex": postHashHex,
                "AppPublicKeyBase58Check": appKey,
                "AssociationType": associationType,
                "AssociationValue": associationValue,
                "MinFeeRateNanosPerKB": self.MIN_FEE,
                "PostExtraData": postExtraData,
            }
            response = requests.post(endpointURL, json=payload)
            transactionHex = response.json()["TransactionHex"]
            seedHexToSignWith = (
                self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            )
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex
                )
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL
            )
            
            return submitTransactionResponse
        
        except Exception as e:
            error = {
                    "error": "Something went wrong while signing the transactions."
                }
            
    def deletePostAssociation(self, transactorKey, association_ID, postExtraData={"Language": "en"}, ):
        postExtraData["App"] = self.appName

        try:
            error = None
            endpointURL = self.NODE_URL + "post-associations/delete"
            finalPostExtraData = postExtraData
            if (
                self.DERIVED_PUBLIC_KEY is not None
                and self.DERIVED_SEED_HEX is not None
                and self.SEED_HEX is None
            ):
                if "DerivedPublicKey" not in finalPostExtraData:
                    finalPostExtraData[
                        "DerivedPublicKey"
                    ] = self.DERIVED_PUBLIC_KEY

            payload = {
                "TransactorPublicKeyBase58Check": transactorKey,
                "associationID": association_ID,
                "PostExtraData": postExtraData,
                "MinFeeRateNanosPerKB": self.MIN_FEE,
            }
            response = requests.post(endpointURL, json=payload)
            print(response.json(), 'first response')
            transactionHex = response.json()["TransactionHex"]
            seedHexToSignWith = (
                self.SEED_HEX if self.SEED_HEX else self.DERIVED_SEED_HEX
            )
            try:
                signedTransactionHex = Sign_Transaction(
                    seedHexToSignWith, transactionHex
                )
            except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }
            submitTransactionResponse = submitTransaction(
                signedTransactionHex, self.NODE_URL
            )
            print(submitTransactionResponse.json(), 'second response')
            
            return submitTransactionResponse
        
        except Exception as e:
                error = {
                    "error": "Something went wrong while signing the transactions. Make sure publicKey and seedHex are correct."
                }