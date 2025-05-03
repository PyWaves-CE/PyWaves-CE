import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest

pw.setThrowOnError(True)

def test_getOrderHistory():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    pw.setMatcher('https://testnet.waves.exchange/api/v1/forward/matcher')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    USDN_WAVES = asset.AssetPair(pw.WAVES, asset.Asset('25FEqEjRkqK6yCkiT7Lz6SAYz7gUFCtxfCChnrVFD5AT'))

    order = myAddress.sell(USDN_WAVES, 100, 1000000000, matcherFee=1000000)
    tx = myAddress.getOrderHistory(USDN_WAVES)
    myAddress.cancelOrder(USDN_WAVES, order)

    assert len(tx) > 0

