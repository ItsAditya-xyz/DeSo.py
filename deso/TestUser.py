"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from User import User


class TestUser(unittest.TestCase):
    """Test the Derived class."""

    def __init__(self, *args, **kwargs):
        super(TestUser, self).__init__(*args, **kwargs)
        self.post_hash = '75b0244b1abc19e3e7ae0cf36f43ecb12588aa30'\
            'ae48db7992edf3fb94d289ad'
        self.nft_post = '2298e051237a8b831aa27d4748d759a8002dd1ab4'\
            '48195ae89d888446ee444e3'
        self.publicReaderKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8Phdge'\
            'ToPn3Fq95RhCMYQVW1Anw'
        self.daoPublicKey = 'BC1YLj3zNA7hRAqBVkvsTeqw7oi4H6ogKiAFL'\
            '1VXhZy6pYeZcZ6TDRY'
        self.pkList = [
            'BC1YLhBLE1834FBJbQ9JU23JbPanNYMkUsdpJZrFVqNGsCe7YadYiUg',
            self.publicReaderKey,
        ]
        self.username = 'deso'
        self.user = User()

    def test_get_user_profile_pubkey(self):
        """Test the getSingleProfile method using public key"""
        try:
            response = self.user.getSingleProfile(
                publicKey=self.publicReaderKey)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetSingleProfile() using node: {self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile_username(self):
        """Test the getSingleProfile method using username"""
        try:
            response = self.user.getSingleProfile(username=self.username)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetSingleProfile() using node: {self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_users_stateless(self):
        """Test the getUsersStateless method"""
        try:
            response = self.user.getUsersStateless(
                listOfPublicKeys=self.pkList
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetUsersStateless() using node: {self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_messages_stateless(self):
        """Test the getMessagesStateless method"""
        try:
            response = self.user.getMessagesStateless(
                publicKey=self.publicReaderKey,
                numToFetch=10,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetMessagesStateless() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_notifications(self):
        """Test the getNotifications method"""
        try:
            response = self.user.getNotifications(
                publicKey=self.publicReaderKey,
                numToFetch=10,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetNotificaitons() using node: {self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_nfts(self):
        """Test the getNFTs method"""
        try:
            response = self.user.getNFTs(
                userPublicKey=self.publicReaderKey,
                isForSale=True
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetNFTs() using node: {self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_derived_keys(self):
        """Test the getDerivedKeys method"""
        try:
            response = self.user.getDerivedKeys(
                publicKey=self.publicReaderKey,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetDerivedKeys() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_transaction_info(self):
        """Test the getTransactionInfo method"""
        try:
            response = self.user.getTransactionInfo(
                publicKey=self.publicReaderKey,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetTransactionInfo() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_holders_for_public_key(self):
        """Test the getHoldersForPublicKey method"""
        try:
            response = self.user.getHoldersForPublicKey(
                self.publicReaderKey,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetHoldersForPublicKey() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_dao_coin_limit_orders(self):
        """Test the getDaoCoinLimitOrders method"""
        try:
            response = self.user.getDaoCoinLimitOrders(
                self.publicReaderKey,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetDaoCoinLimitOrders() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_dao_coin_price(self):
        """Test the getDaoCoinPrice method"""
        try:
            response = self.user.getDaoCoinPrice(
                self.daoPublicKey
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetDaoCoinPrice() using node: '
                f'{self.user.NODE_URL}\n')
        self.assertIsInstance(response, float)

    def test_get_follows_stateless(self):
        """Test the getFollowsStateless method"""
        try:
            response = self.user.getFollowsStateless(
                username=self.username,
                getFollowing=False,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetFollowsStateless(followers) using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

        try:
            response = self.user.getFollowsStateless(
                username=self.username,
                getFollowing=True,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetFollowsStateless(following) using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_diamonds_for_public_key(self):
        """Test the getDiamondsForPublicKey method"""
        try:
            response = self.user.getDiamondsForPublicKey(
                publicKey=self.publicReaderKey,
                received=True,
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetDiamondsForPublicKey(received) using node: '
                f'{self.user.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
