"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from Metadata import Metadata


class TestMetadata(unittest.TestCase):
    """Test the Metadata class."""

    def __init__(self, *args, **kwargs):
        super(TestMetadata, self).__init__(*args, **kwargs)
        self.metadata = Metadata()

    def test_get_exchange_rate(self):
        """Test the getExchangeRate method."""
        try:
            response = self.metadata.getExchangeRate()
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(f'\ngetExchangeRate() using node: '
                             f'{self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_node_health(self):
        """Test the getNodeHealth method."""
        try:
            response = self.metadata.getNodeHealth()
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(f'\ngetNodeHealth() using node: '
                             f'{self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_app_state(self):
        """Test the getAppState method."""
        try:
            response = self.metadata.getAppState()
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(f'\ngetAppState() using node: '
                             f'{self.metadata.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_diamond_level_map(self):
        """Test the getDiamondLevelMap method."""
        try:
            response = self.metadata.getDiamondLevelMap()
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(f'\ngetDiamondLevelMap() using node: '
                             f'{self.metadata.NODE_URL}\n')

        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    unittest.main()
