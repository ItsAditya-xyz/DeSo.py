"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from Posts import Posts


class TestPosts(unittest.TestCase):
    """Test the Posts class."""

    def __init__(self, *args, **kwargs):
        super(TestPosts, self).__init__(*args, **kwargs)
        self.post_hash = '75b0244b1abc19e3e7ae0cf36f43ecb12588aa30ae4'\
            '8db7992edf3fb94d289ad'
        self.nft_post = '2298e051237a8b831aa27d4748d759a8002dd1ab4481'\
            '95ae89d888446ee444e3'
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8PhdgeToP'\
            'n3Fq95RhCMYQVW1Anw'

        self.posts = Posts(readerPublicKey=self.publicReaderKey)

    def test_get_single_post(self):
        """Test the getSinglePost method."""
        try:
            response = self.posts.getSinglePost(self.post_hash)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetSinglePost() using node: {self.posts.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_posts_stateless(self):
        """Test the getPostsStateless method."""
        try:
            response = self.posts.getPostsStateless(
                postHashHex=self.post_hash,
                numToFetch=10,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetPostsStateless() using node: {self.posts.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_posts_for_public_key(self):
        """Test the getPostsForPublicKey method."""
        try:
            response = self.posts.getPostsForPublicKey(
                publicKey=self.publicReaderKey,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetPostsForPublicKey() using node: '
                f'{self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_diamonds_for_post(self):
        """Test the getDiamondsForPost method."""
        try:
            response = self.posts.getDiamondsForPost(
                postHashHex=self.post_hash,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetDiamondsForPost() using node: '
                f'{self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_likes_for_post(self):
        """Test the getLikesForPost method."""
        try:
            response = self.posts.getLikesForPost(
                postHashHex=self.post_hash,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetLikesForPost() using node: {self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_quotereposts_for_post(self):
        """Test the getQuoteRepostsForPost method."""
        try:
            response = self.posts.getQuoteRepostsForPost(
                postHashHex=self.post_hash,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetQuoteRepostsForPost() using node: '
                f'{self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_nft_entries_for_nft_post(self):
        """Test the getNFTEntriesForNFTPost method."""
        try:
            response = self.posts.getNFTEntriesForNFTPost(
                postHashHex=self.nft_post,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetNFTEntriesForNFTPost() using node: '
                f'{self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_nft_bids_for_nft_post(self):
        """Test the getNFTBidsForNFTPostPost method."""
        try:
            response = self.posts.getNFTBidsForNFTPost(
                postHashHex=self.nft_post,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetNFTBidsForNFTPostPost() using node: '
                f'{self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)

    def test_get_hot_feed(self):
        """Test the getHotFeed method."""
        try:
            response = self.posts.getHotFeed()
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetHotFeed() using node: {self.posts.NODE_URL}\n')

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
