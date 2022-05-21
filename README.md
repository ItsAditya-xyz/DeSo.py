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
from decouple import config

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'

desoSocial = deso.Social(nodeURL="https://diamondapp.com/api/v0/",  publicKey = PUBLIC_KEY, seedHex = SEED_HEX)
print(desoSocial.follow("BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg", isFollow=True).json())
```

TODO: Add documentation about other methods

# Deso Identity

1. Validate JWT token

```python
import deso
desoIdentity = deso.Identity()
jwt_tokenn = "" # JWT TOKEN TO VALIDATE
print(desoIdentity.validateJWT(JWT=jwt_token, publicKey=PUBLIC_KEY))
```

TODO: Add more documentation about other methods

# Media

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

# Trade

1. Send deso to public Key

```python
import deso

SEED_HEX = 'YOUR SEED SEED_HEX'
PUBLIC_KEY = 'YOUR PUBLIC_KEY'
desoTrade = deso.Trade(PUBLIC_KEY, SEED_HEX )

print(desoTrade.sendDeso( recieverPublicKeyOrUsername = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg", desoToSend = 0.01))
```
