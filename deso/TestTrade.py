"""
Unit tests for the deso.posts module.
"""
import unittest
import sys
from Trade import Trade


class TestTrade(unittest.TestCase):
    """Test the Trade class."""

    def __init__(self, *args, **kwargs):
        super(TestTrade, self).__init__(*args, **kwargs)
        self.receiverPublicKey = 'BC1YLiy1Ny1btpBkaNHBaUD5D9xX8PhdgeToPn3Fq' \
            '95RhCMYQVW1Anw'
        self.userPublicKey = input("Enter your public key: ")
        self.userSeedHex = input("Enter your seed hex: ")
        self.trade = Trade(self.userPublicKey, self.userSeedHex)

    def test_send_deso(self):
        """Test the sendDeso method."""
        try:
            response = self.trade.sendDeso(
                self.receiverPublicKey,
                desoToSend=0.0001)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetsendDeso() using node: '
                f'{self.trade.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_buy_creator_coin(self):
        """Test the buyCreatorCoin method."""
        try:
            response = self.trade.buyCreatorCoin(
                self.receiverPublicKey,
                desoAmountToBuy=0.0001)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nbuyCreatorCoin() using node: '
                f'{self.trade.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_get_held_coins_of_creator(self):
        """Test the getHeldCoinsOfCreator method."""
        try:
            response = self.trade.getHeldCoinsOfCreator(
                publicKeyOfCoin=self.receiverPublicKey)
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\ngetHeldCoinsOfCreator() using node: '
                f'{self.trade.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_amount_on_sell(self):
        """Test the amountOnSell method."""
        coinsInCirculationNanos = 3857329848
        balanceNanos = 34938
        desoLockedNanos = 12948584035
        amount = None

        amount = self.trade.amountOnSell(
            desoLockedNanos=desoLockedNanos,
            coinsInCirculation=coinsInCirculationNanos,
            balanceNanos=balanceNanos
        )
        self.assertIsInstance(amount, float)

    def test_sell_creator_coin(self):
        """Test the sellCreatorCoin method."""
        coinsToSellNanos = 1
        try:
            response = self.trade.sellCreatorCoin(
                creatorPublicKey=self.receiverPublicKey,
                coinsToSellNanos=coinsToSellNanos
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nsellCreatorCoin() using node: '
                f'{self.trade.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_send_creator_coins(self):
        """Test the sendCreatorCoins method."""
        coinsToSendNanos = 1
        try:
            response = self.trade.sendCreatorCoins(
                creatorPublicKey=self.receiverPublicKey,
                receiverUsernameOrPublicKey="ItsAditya",
                creatorCoinNanosToSend=coinsToSendNanos
            )
        except Exception as e:
            self.fail(e)
        finally:
            sys.stdout.write(
                f'\nsendCreatorCoins() using node: '
                f'{self.trade.NODE_URL}\n')
        self.assertEqual(response.status_code, 200)

    def test_send_dao_coins(self):
        """Test the sendDAOCoins method."""
        coinsToTransfer = 15
        coinsAmountHex = hex(int(coinsToTransfer * 1e18))
        transHex = self.trade.sendDAOCoins(
            coinsToTransfer=coinsAmountHex,
            daoPublicKeyOrName="CockyClout",
            receiverPublicKeyOrUsername="ItsAditya")
        self.assertIsInstance(transHex, hex)

    def test_burn_dao_coins(self):
        """Test the burnDAOCoins method."""
        coinsToBurn = 5000000
        coinsAmountHex = hex(int(coinsToBurn * 1e18))

        transHex = self.trade.burnDAOCoins(
            coinsToBurn=coinsAmountHex,
            daoPublicKeyOrName="CockyClout"
        )
        self.assertIsInstance(transHex, hex)

    def test_mint_dao_coins(self):
        """Test the mintDAOCoins method."""
        coinsToMint = 1000000
        coinsAmountHex = hex(int(coinsToMint * 1e18))

        transHex = self.trade.mintDAOCoins(
            coinsAmountHex
        )
        self.assertIsInstance(transHex, hex)


if __name__ == "__main__":
    unittest.main()
