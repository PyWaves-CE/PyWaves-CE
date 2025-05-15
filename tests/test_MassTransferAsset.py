from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os
import random
import string

PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')

pw.setThrowOnError(True)
helpers = Helpers()
testwallet = helpers.prepareTestcase(101000000, sendTokens=True)

seed = pw.b58encode(os.urandom(32))
recipient1 = address.Address(seed=seed)
seed = pw.b58encode(os.urandom(32))
recipient2 = address.Address(seed=seed)
# use test asset
faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
assets = faucet.assets()
myToken = asset.Asset(assets[0])
# create an address with no balance
seed = pw.b58encode(os.urandom(32))
addressWithNoBalance = address.Address(seed=seed)
# add an extra 1 wves funding to the testwallet

print(f"----- Issuing smart asset -----")
# issue a smart asset
smartAssetName = ''.join(random.choices(string.ascii_lowercase, k=8))
script = 'match tx { \n' + \
                'case _ => true\n' + \
                '}'
tx = testwallet.issueAsset(smartAssetName, f"Test Token {smartAssetName}", 100, 8, reissuable=True)
pw.waitFor(tx['id'])
mySmartAsset = asset.Asset(tx['id'])

try:
    def test_assetMassTransferWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        transfers = [
            {'recipient': recipient1.address, 'amount': 200},
            {'recipient': recipient2.address, 'amount': 200}
        ]
        with pytest.raises(Exception) as error:
            myAddress.massTransferAssets(transfers, myToken)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_assetMassTransferWithTooMuchRecipients():    
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
            testwallet.massTransferAssets(transfers, myToken)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Too many recipients\') tblen=3>'

    def test_feeIsBiggerThanAmountMassTransfer():
        transfers = [
            {'recipient': recipient1.address, 'amount': 200},
            {'recipient': recipient2.address, 'amount': 200}
        ]

        with pytest.raises(Exception) as error:
            addressWithNoBalance.massTransferAssets(transfers, myToken)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'

    def test_amountIsBiggerThanBalanceMassTransfer():
        transfers = [
            {'recipient': recipient1.address, 'amount': 5000000},
            {'recipient': recipient2.address, 'amount': 500000000}
        ]

        with pytest.raises(Exception) as error:
            testwallet.massTransferAssets(transfers, myToken)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Asset balance\') tblen=3>'

    def test_succesfullAssetMassTransfer():
        transfers = [
            {'recipient': recipient1.address, 'amount': 10},
            {'recipient': recipient2.address, 'amount': 10}
        ]
        tx = testwallet.massTransferAssets(transfers, myToken)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_succesfullSmartAssetMassTransfer():
        transfers = [
            {'recipient': recipient1.address, 'amount': 10},
            {'recipient': recipient2.address, 'amount': 10}
        ]
        tx = testwallet.massTransferAssets(transfers, myToken)
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
