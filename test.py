import deso
import json
with open("test.json", "w") as file:
    publicKey = "BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg"
    json.dump(deso.Users.getTransactionInfo(publicKey=publicKey), file)
