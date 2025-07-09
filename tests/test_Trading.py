from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
from pywaves import order
import pytest
import os
import time

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_MATCHER = 'https://testnet.waves.exchange/api/v1/forward/matcher'
pw.setNode(PYWAVES_TEST_NODE, 'T')
pw.setMatcher(PYWAVES_TEST_MATCHER)
helpers = Helpers()
        
try:
    def test_prepareTestcase():
        global testwallet, tokens, A_B
        testwallet = helpers.prepareTestcase(200000000, sendTokens=True)
        tokens = testwallet.assets()
        A_B = asset.AssetPair(asset.Asset(tokens[0]), asset.Asset(assetId=''))
        assert testwallet is not None
        assert tokens is not None
        assert A_B is not None

    def test_orderWithoutStatus():
        orderId = '9JtTmjBqYvrkLuEPmHAJCfuc3cM2FzRNdxH7YKrpz1'
        notExistingOrder = order.Order(orderId, A_B)

        with pytest.raises(Exception) as error:
            testwallet.cancelOrder(A_B, notExistingOrder)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Order not found\') tblen=3>'

    def test_deleteOrderFilled():
        order1 = testwallet.sell(A_B, amount=1, price=1, maxLifetime=15*86400)
        time.sleep(1)
        order2 = testwallet.buy(A_B, amount=1, price=1, maxLifetime=15*86400)
        time.sleep(1)
        with pytest.raises(Exception) as error:
            testwallet.cancelOrder(A_B, order1)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Order already filled\') tblen=3>'

    # place sell orders
    def test_succesfullSellOrder():
        order = testwallet.sell(A_B, amount=1, price=2, maxLifetime=15*86400)
        orderStatus = order.status()
        assert orderStatus == 'Accepted'

    # get order history
    def test_getOrderHistory():
        tx = testwallet.getOrderHistory(A_B)
        
        assert len(tx) > 0

    # buy the previous order
    def test_succesfullBuyOrder():        
        order = testwallet.buy(A_B, amount=1, price=2, maxLifetime=15*86400)
        
        orderStatus = order.status()
        assert orderStatus == 'Filled'

    def test_cancelAllOrders():
        order1 = testwallet.sell(A_B, amount=1, price=3, maxLifetime=15*86400)
        order2 = testwallet.sell(A_B, amount=1, price=4, maxLifetime=15*86400)
        time.sleep(1)
        testwallet.cancelOpenOrders(A_B)
        time.sleep(1)

        assert order1.status() == 'Cancelled' and order2.status() == 'Cancelled'

    def test_cancelOrderById():
        order = testwallet.sell(A_B, amount=1, price=5, maxLifetime=15*86400)
        time.sleep(1)
        testwallet.cancelOrderByID(A_B, order.orderId)
        time.sleep(1)
        assert order.status() == 'Cancelled'

    def test_tradableBalance():
        tradableBalance = testwallet.tradableBalance(A_B)
        A_balance = testwallet.balance(assetId=tokens[0])
        B_balance = testwallet.balance()

        assert tradableBalance == (A_balance, B_balance)

    def test_tradesLimit():
        trades = A_B.trades(10)
        print(trades)
        assert len(trades) > 0

    def test_tradesTimestamp():
        now = int(time.time() * 1000)
        seven_days_ago = now - (7 * 24 * 60 * 60 * 1000)
        trades = A_B.trades(seven_days_ago, now)

        print(trades)
        
    # Dummy test case to return funds to faucet       
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
