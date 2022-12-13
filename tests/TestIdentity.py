"""
Unit tests for the deso.posts module.
"""
import sys
import importlib
import unittest
# making sure we're not importing some other version of deso
# there is certainly a better way to do this, so if you know it
# pls feel free to contribute it :)
MODULE_PATH = "../deso/__init__.py"
MODULE_NAME = "deso"
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
from deso import Identity


class TestIdentity(unittest.TestCase):
    """Test the Metadata class."""

    def __init__(self, *args, **kwargs):
        super(TestIdentity, self).__init__(*args, **kwargs)
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8Phdge' \
            'ToPn3Fq95RhCMYQVW1Anw'
        self.userPublicKey = None
        self.userSeedHex = None
        self.jwt_token = None
        self.identity = Identity(self.publicReaderKey)

    def test_get_JWT(self):
        """Test the getJWT method."""
        self.userPublicKey = input("Enter your public key: ")
        self.userSeedHex = input("Enter your seed hex: ")
        self.identity = Identity(self.userPublicKey, self.userSeedHex)
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
