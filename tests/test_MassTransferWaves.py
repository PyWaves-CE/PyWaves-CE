from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet, recipient1, recipient2
        testwallet = helpers.prepareTestcase()
        seed = pw.b58encode(os.urandom(32))
        recipient1 = address.Address(seed=seed)
        seed = pw.b58encode(os.urandom(32))
        recipient2 = address.Address(seed=seed)

        assert testwallet is not None
        assert recipient1 is not None
        assert recipient2 is not None


    def test_massTransferWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        transfers = [
            {'recipient': recipient1.address, 'amount': 200},
            {'recipient': recipient2.address, 'amount': 200}
        ]

        with pytest.raises(Exception) as error:
            myAddress.massTransferWaves(transfers)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_massTransferWithoutEnoughWaves():
        transfers = [
            {'recipient': recipient1.address, 'amount': 2000000000000000000},
            {'recipient': recipient2.address, 'amount': 2000000000000000000}
        ]

        with pytest.raises(Exception) as error:
            testwallet.massTransferWaves(transfers)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'

    def test_succesfullMassTransfer():
        transfers = [
            {'recipient': recipient1.address, 'amount': 10000},
            {'recipient': recipient2.address, 'amount': 10000}
        ]

        tx = testwallet.massTransferWaves(transfers)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_MassTransferWithTooMuchRecipients():
        transfers = [
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100},
            {'recipient': recipient1.address, 'amount': 100},
            {'recipient': recipient2.address, 'amount': 100}

        ]

        with pytest.raises(Exception) as error:
            testwallet.massTransferWaves(transfers)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Too many recipients\') tblen=3>'
    
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
