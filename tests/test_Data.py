from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import os
import pytest

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase(100000000)

seed = pw.b58encode(os.urandom(32))
address1 = address.Address(seed=seed)

try:
    def test_issueAssetWithoutPrivateKey():
        with pytest.raises(Exception) as error:
            myAddress = address.Address(address1.address)            
            data = [{
                'type': 'string',
                'key': 'test',
                'value': 'testval'
            }]
            tx = myAddress.dataTransaction(data)
       
        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_dataTransactionWithInsufficientWavesBalance():
        with pytest.raises(Exception) as error:
            data = [{
                'type': 'string',
                'key': 'test',
                'value': 'testval'
            }]
            tx = address1.dataTransaction(data)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'
   
    def test_stringDataTransaction():
        data = [{
            'type': 'string',
            'key': 'test',
            'value': 'testval'
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = helpers.waitFor(tx['id'])

        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_integerDataTransaction():
        data = [{
            'type': 'integer',
            'key': 'testint',
            'value': 1234
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = helpers.waitFor(tx['id'])
        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_booleanDataTransaction():
        data = [{
            'type': 'boolean',
            'key': 'test',
            'value': True
        }]
        tx = testwallet.dataTransaction(data)
        blockchainTx = helpers.waitFor(tx['id'])

        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_binaryDataTransaction():
        data = [{
            'type': 'binary',
            'key': 'test',
            'value': 'BzWHaQU'
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = helpers.waitFor(tx['id'])

        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
