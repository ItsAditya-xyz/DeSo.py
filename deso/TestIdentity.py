"""
Unit tests for the deso.posts module.
"""
import unittest
from Identity import Identity


class TestIdentity(unittest.TestCase):
    """Test the Identity class."""

    def __init__(self, *args, **kwargs):
        super(TestIdentity, self).__init__(*args, **kwargs)
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8Phdge' \
            'ToPn3Fq95RhCMYQVW1Anw'
        self.userPublicKey = input("Enter your public key: ")
        self.userSeedHex = input("Enter your seed hex: ")
        self.jwt_token = None
        self.identity = Identity(self.userPublicKey, self.userSeedHex)

    def test_get_JWT(self):
        """Test the getJWT method."""
        self.jwt_token = self.identity.getJWT()
        self.assertIsNotNone(self.jwt_token)

    def test_validate_jwt(self):
        """Test the validateJWT method."""
        v = self.identity.validateJWT(
            JWT=self.jwt_token,
            publicKey=self.userPublicKey
        )
        self.assertTrue(v)

    def test_sign_transaction(self):
        """Test the signTransaction method."""
        transactionHex = input("Enter your transaction hex: ")
        r = self.identity.signTransaction(
            seedHex=self.userSeedHex,
            transactionHex=transactionHex
        )
        self.assertIsNotNone(r)


if __name__ == "__main__":
    unittest.main()
