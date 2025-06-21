from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import os
import random
import string
import time

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')
pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()

# This test case uses directly the faucet in order to save WAVES


try:

    def test_prepareTestcase():
        global faucet
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        assert faucet is not None
        
    def test_updateAssetInfo():
        
        assets = faucet.assets()
        tx = faucet.updateAssetInfo(assets[0], 'pw_testasset-3', 'Description changed by test test_UpdateAssetInfo')
        # updateAssetInfo can be called only after 100000 blocks from the issue transaction
        assert ('error' in tx and 'before' in tx['message']) or ('id' in tx)
            
except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
