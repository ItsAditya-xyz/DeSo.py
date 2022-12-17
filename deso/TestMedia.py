"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from Media import Media


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
            ('file', ('deso.png', open("../deso.png", "rb"), 'image/png'))
        ]
        publicKey = input("Enter your public key: ")
        seedHex = input("Enter your seed hex: ")
        self.media = Media(publicKey, seedHex)
        try:
            response = self.media.uploadImage(imageFileList)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nuploadImage() using node: {self.media.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
