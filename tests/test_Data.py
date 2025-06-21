from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import os
import pytest

helpers = Helpers()


try:
    def test_prepareTestcase():
        global testwallet, address1
        testwallet = helpers.prepareTestcase(100000000)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)

        assert testwallet is not None
        assert address1 is not None

    def test_issueAssetWithoutPrivateKey():
        with pytest.raises(Exception) as error:
            myAddress = address.Address(address1.address)            
            data = [{
                'type': 'string',
                'key': 'test',
                'value': 'testval'
            }]
            tx = myAddress.dataTransaction(data)
       
        assert str(error.value) == 'Private key required'

    def test_dataTransactionWithInsufficientWavesBalance():
        with pytest.raises(Exception) as error:
            data = [{
                'type': 'string',
                'key': 'test',
                'value': 'testval'
            }]
            tx = address1.dataTransaction(data)

        assert str(error.value) == 'Insufficient Waves balance'
   
    def test_stringDataTransaction():
        data = [{
            'type': 'string',
            'key': 'test',
            'value': 'testval'
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = pw.waitFor(tx['id'])

        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_integerDataTransaction():
        data = [{
            'type': 'integer',
            'key': 'testint',
            'value': 1234
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = pw.waitFor(tx['id'])
        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_booleanDataTransaction():
        data = [{
            'type': 'boolean',
            'key': 'test',
            'value': True
        }]
        tx = testwallet.dataTransaction(data)
        blockchainTx = pw.waitFor(tx['id'])

        testwallet.deleteDataEntry(data[0]['key'])
        assert blockchainTx['id'] == tx['id']

    def test_binaryDataTransaction():
        data = [{
            'type': 'binary',
            'key': 'test',
            'value': 'BzWHaQU'
        }]

        tx = testwallet.dataTransaction(data)
        blockchainTx = pw.waitFor(tx['id'])

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
