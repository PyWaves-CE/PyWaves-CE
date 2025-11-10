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
        global testwallet, leasingAddress
        testwallet = helpers.prepareTestcase(100000000)
        seed = pw.b58encode(os.urandom(32))
        leasingAddress = address.Address(seed=seed)
        assert testwallet is not None
        assert leasingAddress is not None

    def test_LeaseAndCheckWavesBalance():
        global testwallet, leasingAddress, leaseTx
        leaseTx = testwallet.lease(leasingAddress, 10000000)
        pw.waitFor(leaseTx['id'])
        print(f"Lease transaction ID: {leaseTx['id']}")
        balance = testwallet.wavesBalance()
        print(balance)
        assert balance['regular'] == 99900000
        assert balance['available'] == 89900000
        assert balance['effective'] == 89900000
        assert balance['generating'] == 0
        balance = leasingAddress.wavesBalance()
        print(balance)
        assert balance['regular'] == 0
        assert balance['available'] == 0
        assert balance['effective'] == 10000000
        assert balance['generating'] == 0

    def test_UnleaseAndCheckWavesBalance():
        global testwallet, leasingAddress, leaseTx
        unleaseTx = testwallet.leaseCancel(leaseTx['id'])
        pw.waitFor(unleaseTx['id'])
        print(f"Unlease transaction ID: {unleaseTx['id']}")
        
    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)

