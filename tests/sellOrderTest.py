from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset

pw.setThrowOnError(True)
pw.setMatcher('https://testnet.waves.exchange/api/v1/forward/matcher')

def test_sellPywavesOffline():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='G6aEiT1ih4jwLfgJ89EvULbsziixDuqnEUTpEkvZ76hv')
    USDN_WAVES = asset.AssetPair(asset.Asset('25FEqEjRkqK6yCkiT7Lz6SAYz7gUFCtxfCChnrVFD5AT'), asset.Asset('WAVES'))

    pw.setOffline()
    tx = myAddress.sell(USDN_WAVES, 10, 4600)
    pw.setOnline()

    assert tx['api-type'] == 'POST'

def test_succesfullSellOrder():
    pw.setMatcher('https://testnet.waves.exchange/api/v1/forward/matcher')
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    USDN_WAVES = asset.AssetPair(pw.WAVES,asset.Asset('25FEqEjRkqK6yCkiT7Lz6SAYz7gUFCtxfCChnrVFD5AT'))

    order = myAddress.sell(USDN_WAVES, 100, 1000000000, matcherFee=1000000)
    orderStatus = order.status()

    myAddress.cancelOrder(USDN_WAVES, order)
    assert orderStatus == 'Accepted'