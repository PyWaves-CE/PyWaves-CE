from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
import pytest
import os
import random
import string

pw.setThrowOnError(True)
helpers = Helpers()

try:

    def test_prepareTestcase():
        global testwallet, address1, token
        testwallet = helpers.prepareTestcase(201000000)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)
        assetName = ''.join(random.choices(string.ascii_lowercase, k=8))
        token = testwallet.issueAsset(assetName, f"Test Token {assetName}", 100*(10**8), 8, reissuable=True)
        pw.waitFor(token['id'])

        assert testwallet is not None
        assert address1 is not None
        assert token is not None

    def test_sponsoringAssetWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        with pytest.raises(Exception) as error:
            myAddress.sponsorAsset(token, minimalFeeInAssets = 1)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_succesfullSponsoringAsset():
        
        tx = testwallet.sponsorAsset(token['id'], minimalFeeInAssets = 1  )
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)