# DesoPy - A python module to intereact with DeSo Blockchain

Developed by [ItsAditya](https://diamondapp.com/u/itsaditya)

Run `pip install deso` to install the module!

## How to Use:

### Metadata

1. Getting Deso Price

```python
import deso

# takes two optional Argument; publicKey and nodeURL. By default NodeURL is https://node.deso.org/api/v0/"
desoMetadata = deso.Metadata()
response = desoMetadata.getExchangeRate() # returns a response object.
print(response.json()) #  you can also use response.status_code to check if request was succesful
```

2. Getting Node Health

```python
import deso
desoMetadata = deso.Metadata()
print(desoMetadata.getNodeHealth().json())
```

3. Getting App State which includes node fee, diamond level map and other info related to node

```python
import deso
desoMetadata = deso.Metadata()
print(desoMetadata.getAppState().json())
```

4. Getting value of each diamond

```python
import deso
desoMetadata = deso.Metadata()
print(desoMetadata.getDiamondLevelMap()) # getDiamondLevelMap takes optional inDesoNanos argument which is by default True.
```

### User

1. Getting user profile

```python
import deso
desoUser = deso.User()
print(desoUser.getSingleProfile(username="ItsAditya").json())
# you can set username to "" and use publicKey instead. Like: getSingleProfiel(publicKey = "BBC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg")
```

2. Getting publicKey info

```python
import deso
desoUser = deso.User()
publicKeyList = ["BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg",
    "BC1YLhGyi3t6ppCMARk3pmXGTkrSJXw3GWxQsYwQp58897ho8Nbr1it"]
print(desoUser.getUsersStateless(listOfPublicKeys=publicKeyList).json())
```

3. Getting profile pic URL

```python
import deso
desoUser = deso.User()
print(desoUser.getProfilePicURL(
    "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"))
```

4. Getting User Messages

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getMessagesStateless(
    publicKey=userPublicKey, numToFetch=10).json())
# There are more argument in getMessagesStateless like sortAlgorithm, followersOnly, followingOnly, holdersOnly, holdingsOnly, fetchAfterPublicKey
```

5. Getting user notifications

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getNotifications(userPublicKey, numToFetch=1000).json())
# There are other argument in getNotifications() like startIndex, filterOutNotificationCategories, etc.
```

6. Getting User NFTs

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getNFTs(userPublicKey = userPublicKey, isForSale=True).json())
```

7.  Get derived keys of a user

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getDerivedKeys(userPublicKey).json())
```

8. Getting transaction info of a user

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getTransactionInfo(userPublicKey).json())
# There are other arguments in getTransactionInfo() like limit, lastPublicKeyTransactionIndex and lastTransactionIDBase58Check
```

9. Getting holders for a public key

```python
import deso
desoUser = deso.User()
userPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getHoldersForPublicKey(userPublicKey).json())
# There are other arugments in getHoldersForPublicKey like username, fetchAll, numToFetch, fetchHodlings, isDAOCOIN, lastPublicKey
```

10. Getting DAO coin limit orders of a DAO coin

```python
import deso
desoUser = deso.User()
daoCoinPublicKey = "BC1YLj3zNA7hRAqBVkvsTeqw7oi4H6ogKiAFL1VXhZy6pYeZcZ6TDRY"
print(desoUser.getDaoCoinLimitOrders(daoCoinPublicKey))
```

11. Geting user followings/followers

```python
import deso
desoUser = deso.User()
print(desoUser.getFollowsStateless(username = "ItsAditya").json())
```

12. Getting diamonds sent/received by a publicKey
```python
import deso

desoUser = deso.User()
publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoUser.getDiamondsForPublicKey(publicKey, received=False).json())
# set received = True to get diamonds given to a publicKey
```
### Posts

1. Get posts stateless - getting info about post

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getPostsStateless(postHashHex= postHashHex, numToFetch=10).json())

# There are other functions in getPostsStateless that can be used to get more information about a post.
```

2. Get single post information

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getSinglePost(postHashHex).json())
# There are other functions in getSinglePost() that can be used to get more information about a post.
```

3. Get posts by publicKey or user

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getPostsForPublicKey(username="ItsAditya").json())
# getPostsForPublicKey() has more arguments like publicKey, mediaRequired, numToFetch, lastPostHashHex, readerPublicKey etc.
```

4. Get serials of NFT post include other info

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getNFTEntriesForNFTPost(postHashHex).json())
```

5. Get likes for post

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getLikesForPost(postHashHex).json())
# getLikesForPost has more arguments like limit, offset etc.
```

6. Get diamonds for post

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getDiamondsForPost(postHashHex).json())
# getDiamondsForPost has more arguments like limit, offset etc.
```

7. Get getQuoteRepostsForPost for post

```python
import deso

desoPosts = deso.Posts()
postHashHex = "74d50e4d33b7512941a2ada91a947aecfc2f9fd179d67eb1e0008d4812597196"
print(desoPosts.getQuoteRepostsForPost(postHashHex).json())
# getQuoteRepostsForPost has more arguments like limit, offset etc.
```

8. Get Hot feed/ Posts mentioning any @ username

```python
import deso
desoPosts = deso.Posts()
print(desoPosts.getHotFeed(taggedUsername="ItsAditya").json())
```

### Social

1. Making post to deso blockchain

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'
desoSocial = deso.Social(PUBLIC_KEY, SEED_HEX)
'''In the above deso.Social() constructor, you can pass `derivedPublicKey` and `derivedSeedHex`
to make the transactions using derived keys.
NOTE: YOU MUST PASS ORIGINAL PUBLIC KEY TO CREATE THE TRANSACTION
''''

# submitPost() takes many optional argument like imageURLs, videoURLs, postExtraData etc.
# you will use the same function to make comment and quote any post.
print(desoSocial.submitPost("This is a test post")) #returns a response object. add .json() in end to see complete response
```

2. Follow user

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/",  publicKey = PUBLIC_KEY, seedHex = SEED_HEX)
print(desoSocial.follow("BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg", isFollow=True).json())
```

3. Repost a post

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHexToRepost = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.repost(postHashHexToRepost).json())
```

4. Like a post

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.like(postHashHex, isLike=True).json())
```

5. Diamond a post

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
receiverPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoSocial.diamond(postHashHex, receiverPublicKey,  diamondLevel=2).json())
```

6. Update Profile

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
print(desoSocial.updateProfile(FR=10, description="This is my description",
      username="NotItsAditya", profilePicBase64='').json())


# In the above example, make sure profilePicBase64 is BASE64 encoded image otherwise it wont' work.
```

7. Send Private Message

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
receiverPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoSocial.sendPrivateMessage(receiverPublicKey, "This DM is send using DesoPy library").json())
```

8. Minting a postHashHex as NFT

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.mint(postHashHex, minBidDeSo=1, copy=2, creatorRoyality=10, coinHolderRoyality=4, isForSale=True).json())
```

9. Updating NFT to put it on sale, or as buy now etc.

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.updateNFT(postHashHex, buyNowPriceInDeso=2,
      buyNow=True, minBidDeso=1.5, forSale=2, serialNumber=1).json())
```

10. Burn an NFT

```python

import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.burnNFT(postHashHex, serialNumber=2).json())
```

11. Create NFT Bid

```python

import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
print(desoSocial.createNFTBid(NFTPostHashHex=postHashHex, serialNumber=1, bidAmountDeso=2).json())
```

12. Transfer NFT

```python

import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
postHashHex = "bd292216e8cc1b7f2dd2cc6bba5afa20b65a4b9966ea191644c90254bedbe177"
receiverPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoSocial.transferNFT(postHashHex, receiverPublicKey, serialNumber=1).json())
```

### Deso Identity

1. Getting JWT token

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoIdentity = deso.Identity(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
print(desoIdentity.getJWT())
```

2. Validate JWT token

```python
import deso
desoIdentity = deso.Identity()
jwt_tokenn = "" # JWT TOKEN TO VALIDATE
userPublicKey = "" # User's public Key whoose JWT you wanna validate
print(desoIdentity.validateJWT(JWT=jwt_token, publicKey=userPublicKey))
```

3. Sign transaction (OFFLINE OBVIOUSLY)

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
transactionHex = " Transaction Hex of the transaction created by public Key"
desoIdentity = deso.Identity()
print(desoIdentity.signTransaction(seedHex = SEED_HEX, transactionHex=transactionHex))
```

### Media

1. Upload iamge to images.deso.org

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'
desoMedia = deso.Media(  PUBLIC_KEY, SEED_HEX)
imageFileList = [
    ('file', ('screenshot.jpg', open("img.png", "rb"), 'image/png'))
]  # 'imageToUpload.png' is the image we are uploading to images.bitclout.com
urlResponse = desoMedia.uploadImage(imageFileList)
print(urlResponse.json())
```

### Trade

1. Send deso to public Key

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'
desoTrade = deso.Trade(PUBLIC_KEY, SEED_HEX )

print(desoTrade.sendDeso( recieverPublicKeyOrUsername = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg", desoToSend = 0.01).json())
```

2. Buy creator coin

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoTrade = deso.Trade(PUBLIC_KEY, SEED_HEX)
creatorPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoTrade.buyCreatorCoin(creatorPublicKey=creatorPublicKey, desoAmountToBuy=2).json())
```

3. get creator coins held by a publicKey

```python
import deso

desoTrade = deso.Trade()
creatorPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoTrade.getHeldCoinsOfCreator(publicKeyOfCoin=creatorPublicKey).json())
```

4. Get selling amount of a creator coin

```python
import deso
desoTrade = deso.Trade()
coinsInCirculationNanos = 3857329848
balanceNanons = 34938
desoLockedNanos = 12948584035
print(desoTrade.amountOnSell(desoLockedNanos = desoLockedNanos, coinsInCirculation=coinsInCirculationNanos, balanceNanos=balanceNanos))
```

5. Selling a creator coin

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoTrade = deso.Trade(PUBLIC_KEY, SEED_HEX)

coinsToSellNanons = 34938
creatorPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoTrade.sellCreatorCoin(
    creatorPublicKey=creatorPublicKey,  coinsToSellNanos=coinsToSellNanons).json())
```

6. Send creator coin

```python
import deso
SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoTrade = deso.Trade(PUBLIC_KEY, SEED_HEX)

coinsToSendNanos = 34938
creatorPublicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
print(desoTrade.sendCreatorCoins(creatorPublicKey=creatorPublicKey,
      receiverUsernameOrPublicKey="Octane", creatorCoinNanosToSend=coinsToSendNanos).json())
```

7. Send DAO coins

```python
import deso
SEED_HEX = "Your seed Hex here"
PUBLIC_KEY = "Your public key"

'''Sends DAO coin to publicKey or username. Use the hex() function to convert a number to hexadecimal
for Example, if you want to send 15 DAO coin, set coinsToTransferNanosInHex to hex(int(15*1e18))'''
desoTrade = deso.Trade(publicKey=PUBLIC_KEY, seedHex=SEED_HEX)
coinsToTransfer = 15
coinsToTransferInRequiredForamt = hex(int(coinsToTransfer * 1e18))
transferStatus = desoTrade.sendDAOCoins(coinsToTransfer=coinsToTransferInRequiredForamt,
                                        daoPublicKeyOrName="CockyClout", receiverPublicKeyOrUsername="ItsAditya")
print(transferStatus)
```
