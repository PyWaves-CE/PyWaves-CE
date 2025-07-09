import pywaves as pw
from pywaves import address
import pytest
from tests.helpers import Helpers
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
helpers = Helpers()
testwallet = None

try:

    def test_prepareTestcase():
        global testwallet
        testwallet = helpers.prepareTestcase(100000000)
        assert testwallet is not None

    def test_addressWithoutScript():
        result = testwallet.script()
        print(result)
        assert (result['script'] is None and result['extraFee'] == 0)

    def test_adddressWithScript():
        script = '''{-# STDLIB_VERSION 6 #-}
        {-# CONTENT_TYPE DAPP #-}
        {-# SCRIPT_TYPE ACCOUNT #-}

        @Callable(inv)
        func default() = {
            let message = "Hello from RIDE contract!"
            [
                StringEntry("lastMessage", message),
                StringEntry("caller", inv.caller.toString())
            ]
        }'''

        tx = testwallet.setScript(script, txFee=500000)
        pw.waitFor(tx['id'])

        result = testwallet.script()
        print(result)
        assert (result['script'].startswith('base64:') and result['extraFee'] == 0)

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
