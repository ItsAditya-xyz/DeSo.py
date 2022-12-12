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
from deso import Metadata


class TestMetadata(unittest.TestCase):
    """Test the Metadata class."""

    def __init__(self, *args, **kwargs):
        super(TestMetadata, self).__init__(*args, **kwargs)
        self.post_hash = '75b0244b1abc19e3e7ae0cf36f43ecb12588aa30ae48db7992edf3fb94d289ad'
        self.nft_post = '2298e051237a8b831aa27d4748d759a8002dd1ab448195ae89d888446ee444e3'
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8PhdgeToPn3Fq95RhCMYQVW1Anw'
        self.username = 'deso'
        self.metadata = Metadata()

    def test_get_exchange_rate(self):
        """Test the getExchangeRate method."""
        try:
            response = self.metadata.getExchangeRate()
        finally:
            sys.stdout.write(f'\ngetExchangeRate() using node: {self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_node_health(self):
        """Test the getNodeHealth method."""
        try:
            response = self.metadata.getNodeHealth()
        finally:
            sys.stdout.write(f'\ngetNodeHealth() using node: {self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_app_state(self):
        """Test the getAppState method."""
        try:
            response = self.metadata.getAppState()
        finally:
            sys.stdout.write(f'\ngetAppState() using node: {self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_diamond_level_map(self):
        """Test the getDiamondLevelMap method."""
        try:
            response = self.metadata.getDiamondLevelMap()
        finally:
            sys.stdout.write(f'\ngetDiamondLevelMap() using node: {self.metadata.NODE_URL}\n')

        self.assertIsInstance(response, dict)




if __name__ == "__main__":
    unittest.main()
