from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os
import base58

pw.setThrowOnError(True)

helpers = Helpers()
testwallet = helpers.prepareTestcase()

seed = str(base58.b58encode(os.urandom(32)))
leasingAddress = address.Address(seed=seed)
seed = str(base58.b58encode(os.urandom(32)))
leasingAddressWithNoBalance = address.Address(seed=seed)
leasingId = str(base58.b58encode(os.urandom(32)))

try:

    def test_cancelWithoutPrivateKey():
        myAddress = address.Address('3MpvqThrQUCC1DbkY9sMmo4fp77e2h11NaM')

        with pytest.raises(Exception) as error:
            myAddress.leaseCancel(leasingId)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'
    
    def test_cancelWithFeeIsBiggerThanBalance():
        with pytest.raises(Exception) as error:
            leasingAddressWithNoBalance.leaseCancel(leasingId)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'
        
    def test_succesfullCancelLeasing():
        leaseTransaction = testwallet.lease(leasingAddress, 900000)
        helpers.waitFor(leaseTransaction['id'])        
        tx = testwallet.leaseCancel(leaseTransaction['id'])
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']
    
    def test_pywavesOffline():
        pw.setOffline()
        leaseCancelTransactionId = testwallet.leaseCancel(leasingId)
        pw.setOnline()

        assert leaseCancelTransactionId['api-type'] == 'POST'
    
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)