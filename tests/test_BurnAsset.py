import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from random import randint
from tests.helpers import Helpers
import os

helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet
        testwallet = helpers.prepareTestcase(sendTokens=True)
        assert testwallet is not None

    def test_succesfullBurnAsset():
        tokens = testwallet.assets()
        myToken = asset.Asset(tokens[0])
        tx = testwallet.burnAsset(myToken, 1)
        blockchaintx = pw.waitFor(tx['id'])
        
        assert blockchaintx['id'] == tx['id']
        
    def test_pywavesOfflineBurnAsset():
        tokens = testwallet.assets()
        myToken = asset.Asset(tokens[0])
        pw.setOffline()       
        tx = testwallet.burnAsset(myToken, 1)
        pw.setOnline()

        assert tx['api-type'] == 'POST'

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)

