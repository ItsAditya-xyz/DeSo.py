"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from Social import Social


class TestSocial(unittest.TestCase):
    """Test the Metadata class."""

    def __init__(self, *args, **kwargs):
        super(TestSocial, self).__init__(*args, **kwargs)
        self.post_hash = '75b0244b1abc19e3e7ae0cf36f43ecb12588aa30ae48' \
            'db7992edf3fb94d289ad'
        self.nft_post = '2298e051237a8b831aa27d4748d759a8002dd1ab44819' \
            '5ae89d888446ee444e3'
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8PhdgeToPn' \
            '3Fq95RhCMYQVW1Anw'
        self.username = 'deso'
        self.userPublicKey = input("Enter your public key: ")
        self.userSeedHex = input("Enter your seed hex: ")

        self.social = Social(self.userPublicKey, self.userSeedHex)

    def test_submit_post(self):
        """Test the submitPost method."""
        try:
            response = self.social.submitPost(
                "This is a test post"
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nsubmitPost() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_follow(self):
        """Test the follow method."""
        try:
            response = self.social.follow(
                self.publicReaderKey,
                isFollow=True
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nfollow() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_repost(self):
        """Test the repost method."""
        try:
            response = self.social.repost(self.post_hash)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nrepost() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_quote(self):
        """Test the quote method."""
        body = "This is a test quote"
        try:
            response = self.social.quote(
                body, self.post_hash
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nquote() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_like(self):
        """Test the like method."""
        try:
            response = self.social.like(self.post_hash, isLike=True)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nlike() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_diamond(self):
        """Test the diamond method."""
        try:
            response = self.social.diamond(
                self.post_hash,
                self.publicReaderKey,
                diamondLevel=1
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ndiamond() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        """Test the updateProfile method."""
        try:
            response = self.social.updateProfile(
                FR=10, description="This is my new description",
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nsubmitPost() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_send_private_message(self):
        """Test the sendPrivateMessage method."""
        try:
            response = self.social.sendPrivateMessage(
                self.publicReaderKey,
                "It goes down in the DM!")
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nsendPrivateMessage() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_mint(self):
        """Test the mint method."""
        try:
            response = self.social.mint(
                self.post_hash,
                minBidDeSo=1, copy=2, creatorRoyalty=10,
                coinHolderRoyalty=4, isForSale=True
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nmint() using node: {self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_update_nft(self):
        """Test the updateNFT method."""
        try:
            response = self.social.updateNFT(
                self.nft_post,
                buyNowPriceInDeso=2,
                buyNow=True,
                minBidDeso=1.5,
                forSale=2,
                serialNumber=1
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nupdateNFT() using node: {self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_burn_nft(self):
        """Test the burnNFT method."""
        try:
            response = self.social.burnNFT(
                self.nft_post,
                serialNumber=2
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nburnNFT() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_create_nft_bid(self):
        """Test the createNFTBid method."""
        try:
            response = self.social.createNFTBid(
                NFTPostHashHex=self.nft_post,
                serialNumber=1,
                bidAmountDeso=2
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ncreateNFTBid() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_transfer_nft(self):
        """Test the transferNFT method."""
        try:
            response = self.social.transferNFT(
                self.nft_post,
                self.publicReaderKey,
                serialNumber=2
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ntransferNFT() using node: '
                f'{self.social.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
