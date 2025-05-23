from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase(100000000)

seed = pw.b58encode(os.urandom(32))
print(f"Using seed: {seed}")
leasingAddress = address.Address(seed=seed)

try:
    def test_leasingWithoutPrivateKey():
        myAddress = address.Address('3MpvqThrQUCC1DbkY9sMmo4fp77e2h11NaM')
        with pytest.raises(Exception) as error:
            myAddress.lease(leasingAddress, 10000000)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_leasingWithAmountSmallerEqualsZero():        
        with pytest.raises(Exception) as error:
            testwallet.lease(leasingAddress, -10000000)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Amount must be > 0\') tblen=3>'

    def test_balanceSmallerThanAmount():
        with pytest.raises(Exception) as error:
            testwallet.lease(leasingAddress, 10000000000000000000000)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'

    def test_succesfullLeasing():
        tx = testwallet.lease(leasingAddress, 100000)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

        testwallet.leaseCancel(tx['id'])
        blockchainTx = pw.waitFor(tx['id'])
        
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
