from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import os

PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')

pw.setThrowOnError(True)
helpers = Helpers()

def test_prepareTestcase():
    global faucet, myToken
    faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
    assets = faucet.assets()
    myToken = asset.Asset(assets[0])
    assert faucet is not None
    assert myToken is not None

def test_succesfullReissueAsset():
    tx = faucet.reissueAsset(myToken, 10, reissuable=True)
    blockchaintx = pw.waitFor(tx['id'])

    assert blockchaintx['id'] == tx['id']

def test_reissueAssetPywavesOffline():   
    pw.setOffline()
    tx = faucet.reissueAsset(myToken, 10, reissuable=True)
    pw.setOnline()
    assert tx['api-type'] == 'POST'

