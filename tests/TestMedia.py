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
from deso import Media


class TestMedia(unittest.TestCase):
    """Test the Media class."""

    def __init__(self, *args, **kwargs):
        super(TestMedia, self).__init__(*args, **kwargs)
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8PhdgeToPn' \
            '3Fq95RhCMYQVW1Anw'
        self.media = Media()

    def test_upload_image(self):
        """Test the uploadImage method."""
        imageFileList = [
            ('file', ('screenshot.jpg', open("deso.png", "rb"), 'image/png'))
        ]
        publicKey = input("Enter your public key: ")
        seedHex = input("Enter your seed hex: ")
        self.media = Media(publicKey, seedHex)
        try:
            response = self.media.uploadImage(imageFileList)
        except Exception as e:
            self.fail(e)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
