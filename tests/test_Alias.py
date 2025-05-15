from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
import random
import string
import pytest
import os

pw.setThrowOnError(True)

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase()
alias = ''.join(random.choices(string.ascii_lowercase, k=8))

seed = pw.b58encode(os.urandom(32))
address1 = address.Address(seed=seed)

try:

    def test_aliasWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        with pytest.raises(Exception) as error:
            myAddress.createAlias(alias)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_succesfullAlias():
        tx = testwallet.createAlias(alias)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']
    
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
