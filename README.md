# DeSo.py

A python package for DeSo.

Developed by [ItsAditya](https://bitclout.com/u/itsaditya)

Run `pip install deso` to install the module!

## Examples of How To Use DeSo.py

### Getting $DeSo price

```python
import deso
print(deso.Deso.getDeSoPrice())
```

### Getting user(s) info through publicKey(s)

```python
import deso
import json
with open("userInfo.json", "w") as file:
    listOfPublicKeys = ["BC1YLjJVhcVAi5UCYZ2aTNwRMtqvzQar4zbymr7fyinu8MsWLx2A1g1"] # you can pass multiple public key of users
    json.dump(deso.Users.getUserStateless(listOfPublicKeys), file)
```

### Getting user info through DeSo username

```python
import deso
import json
with open("userInfo.json", "w") as file:
    username = "ItsAditya" 
    json.dump(deso.Users.getSingleProfile(username=username), file) #you can also pass publicKey = "<public key of any user>" here instead of username just in case you want to get the profile info from public key
```

### Getting profile pic through public key

```python
import deso
publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg" # well, that's my (@ItsAditya) public key :)
print(deso.Users.getProfilePic(publicKey))
```

### Getting wallet of a user through public key

```python
import deso
import json
publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg" 
with open("wallet.json", "w") as file:
    walletData = deso.Users.getWallet(publicKey, includeCreatorCoin = True) # make includeCreatorCoin as false when you don't want to have creator coin investment in the response data
    json.dump(walletData, file)
```

### getting creator coin holders of a user

```python
import deso 
import json
publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
with open("investors.json", "w") as file:
    investorData = deso.Users.getHodlers( username =  "", publicKey= publicKey, lastPublicKey= "", numToFetch = 100, fetchAll = False)
    # well, you can play around with above list of args to get what you want :)
    json.dump(investorData, file) 
```

### Getting users who are blocked by a profile

```python
import deso
import json
with open("blockedUsers.json", "w") as file:
    publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg" # well, that's my (@ItsAditya) public key :)
    json.dump(deso.Users.getUsersBlocked(publicKey), file)
```

### Getting user posts

```python
import deso
import json
with open("UserPosts.json", "w") as file:
    json.dump(deso.Posts.getUserPosts(username="ItsAditya"), file)
```

### Getting information about single post ( likes, comments etc on a post)

```python
import deso
import json
with open("UserPosts.json", "w") as file:
    postHash = "52f9b2dc7f616a94d583a5a167bb49ba7558279e06bdd0642b1777246a6570a2" #the hash of the post. you can find this in post URL :)

    postInfo = deso.Posts.getPostInfo(postHash, commentLimit = 20, fetchParents = False, commentOffset = 0, addGlobalFeedBool = False, readerPublicKey = "BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB")
    json.dump(postInfo, file)
```

#### Getting diamond information about a user (received or sent)

```python
import deso
import json
with open("diamondsReceived.json", "w") as file:
    publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
    diamondData = deso.Diamonds.getDiamonds(publicKey=publicKey, received=True)
    '''reveived is an optional arguement when true it returns diamond received by users else
    return diamonds give by users'''
    json.dump(diamondData, file)
```

### Getting deleted posts of a user

```python
import deso
import json

#public Key of @DiamondHands
publicKey = "BC1YLgU67opDhT9bTPsqvue9QmyJLDHRZrSj77cF3P4yYDndmad9Wmx" 
with open("HiddenPosts.json", "w") as file:
    json.dump(deso.Posts.getHiddenPosts(publicKey), file)
```


### Buying creator coin of a user

```python
from deso import *

''' SEEDHEX should always be kept private. It has access to your complete wallet. It's kinda like
    seed phrase. This is why writing methods in backend isn't a good practice until we have derived keys.
    You can only automate your own account and can't have user authorisation. It is recommended to use test account while using write methods.

    You can find the seedHex of your account in your browser storage. Just open https://bitclout.com/ > Dev tools > Application > Storage > Local Storage > https://identity.bitclout.com > users > Select the public key with which you want to post > seedHex'''
SEEDHEX = "" # you seedHex
PUBLIC_KEY = "" #you PublicKey


PublicKeyToBuy = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg" 
trade = Trade(SEEDHEX, PUBLIC_KEY)
status = trade.buy(keyToBuy = PublicKeyToBuy, DeSo = 0.1) # you are buying 0.1 DeSO of the creator's coin
print(status)  #200 if transaction was succesfull
```

### Selling creator coin of a user

```python
from deso import *

''' SEEDHEX should always be kept private. It has access to your complete wallet. It's kinda like
    seed phrase. This is why writing methods in backend isn't a good practice until we have derived keys.
    You can only automate your own account and can't have user authorisation. It is recommended to use test account while using write methods.

    You can find the seedHex of your account in your browser storage. Just open https://bitclout.com/ > Dev tools > Application > Storage > Local Storage > https://identity.bitclout.com > users > Select the public key with which you want to post > seedHex'''
SEEDHEX = "" # you seedHex
PUBLIC_KEY = "" #you PublicKey


publicKeyToSell = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg" 
trade = Trade(SEEDHEX, PUBLIC_KEY)
status = trade.sell(keyToSell = publicKeyToSell, sellMax = True)# you are selling max coins of the creator
print(status)  #200 if transaction was succesfull
```

### Sending a post on deso

```python
from deso import Post

''' SEEDHEX should always be kept private. It has access to your complete wallet. It's kinda like
    seed phrase. This is why writing methods in backend isn't a good practice until we have derived keys.
    You can only automate your own account and can't have user authorisation. It is recommended to use test account while using write methods.

    You can find the seedHex of your account in your browser storage. Just open https://bitclout.com/ > Dev tools > Application > Storage > Local Storage > https://identity.bitclout.com > users > Select the public key with which you want to post > seedHex'''
SEEDHEX = ""  # your seedHex
PUBLIC_KEY = ""  # your PublicKey

post = Post(SEEDHEX, PUBLIC_KEY)

status = post.send("This post was sent using the DeSo python library 😎")
print(status)  # 200 if post was successfull
```

### Uploading image on images.bitclout.com
```python
from deso import Post

''' SEEDHEX should always be kept private. It has access to your complete wallet. It's kinda like
    seed phrase. This is why writing methods in backend isn't a good practice until we have derived keys.
    You can only automate your own account and can't have user authorisation. It is recommended to use test account while using write methods.

    You can find the seedHex of your account in your browser storage. Just open https://bitclout.com/ > Dev tools > Application > Storage > Local Storage > https://identity.bitclout.com > users > Select the public key with which you want to post > seedHex'''
SEEDHEX = ""  # your seedHex
PUBLIC_KEY = ""  # your PublicKey

post = Post(SEEDHEX, PUBLIC_KEY)
imageFileList=[
  ('file',('screenshot.jpg',open("imageToUpload.png", "rb"),'image/png'))
] # 'imageToUpload.png' is the image we are uploading to images.bitclout.com
urlResponse = post.uploadImage(imageFileList)
print(urlResponse) # sample response: {"ImageURL":"https://images.bitclout.com/654c5d57a6f61b053290e232daa8242b7b3f156df20dacac0d20c6b00e0aeb18.webp"}
```
### Posting image on arweave
```python
import deso
#arweave.json is the JSON file of you arweave wallet. Get one at ardrive.io
arweaveURL = deso.Nft.uploadToArweave(
    wallet = "arweave.json",
    image = "image.png"
)
print(arweaveURL) # returns arweave image URL
```

### Minting NFT on deso
```python

import deso
SEED_HEX = "" #your seed hex
PUBLIC_KEY  = "" #Your public key
#uploading image to arweave. Here arweave.json is your arweave wallet JSON file. Get one at ardrive.io
arweaveURL = deso.Nft.uploadToArweave(
    wallet = "arweave.json",
    image = "image.png"
)
#posting image on DeSo
post = deso.Post(SEED_HEX, PUBLIC_KEY)
postResponse = post.send("This is the test NFT made by DeSo.py SD",
                     imageUrl=[str(arweaveURL)])
postHashHex = postResponse["postHashHex"]
status = post.mint(postHashHex, minBidDeSo=0.1, copy = 10)
if status == 200:
    print(f"NFT is live at https://diamondapp.com/nft/{postHashHex}")
else:
    print(status)
```

### Sending direct message on DeSo
```python
from deso import Message
import json

SEEDHEX = "" # your seed Hex
PUBLIC_KEY = "" #your public Key
msg = Message(SEEDHEX, PUBLIC_KEY)
text = "This is a direct message made using DeSo.py"
recipientKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
status = msg.send(recipientKey, text)
print(status)  # 200 if post was successfulld
```

### Getting NFT entries for NFT postHash
```python
from deso import Nft
import json
postHashHex = "d017e4a6f9a7975777f6a4f5b55074590013f362344b8928d1a1a6fcdbe10aca"
with open("NftPostInfo.json", "w") as file:
     niftyInfo = deso.Nft.getNFT(postHashHex)
     json.dump(niftyInfo, file)
```    
### Getting (recent) Transaction info of public key 
```python
import deso
import json
with open("test.json", "w") as file:
    publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
    json.dump(deso.Users.getTransactionInfo(publicKey=publicKey), file)
    #by default this function returns last 200 transactions, you can play around with the parameters :
```

### Getting Notifications of user through public Key
```python
import deso
import json

with open("test.json", "w") as file:
    publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
    json.dump(deso.Users.getNotifications(publicKey= publicKey), file)
    #by defualt it returns last 50 notifs. You can play with the arguments :)

```

More docs coming soon!

Found any issue ? Report us on our [repo](https://github.com/AdityaChaudhary0005/DeSo.py)

Tip the author of this module some $DeSo at: [@ItsAditya](https://bitclout.com/u/ItsAditya) (even 1 diamond counts :)