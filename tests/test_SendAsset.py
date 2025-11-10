from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet, myToken
        testwallet = helpers.prepareTestcase(sendTokens=True)
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        assets = faucet.assets()
        myToken = asset.Asset(assets[0])
        
        assert testwallet is not None
        assert myToken is not None


    # no need to use testwallet, just use the address
    def test_assetTransactionWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        with pytest.raises(Exception) as error:
            myAddress.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 3)

        assert str(error.value) == 'Private key required'

    def test_assetTransactionWithAmountSmallerEqualsZero():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, -1)

        assert str(error.value) == 'Amount must be > 0'

    def test_nonExistantAssetTransaction():
        myToken = asset.Asset('Test')
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 1)

        assert str(error.value) == 'Asset not issued'

    def test_assetTransactionButAmountBiggerThanBalance():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5000000000)

        assert str(error.value) == 'Insufficient Asset balance'
   
    def test_transactionWithNoAsset():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), None, 100000000000000000)

        assert str(error.value) == 'Insufficient Waves balance'
  
    def test_successfulTransactionWithSponsoredFee():
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, feeAsset = myToken, txFee=1)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_succesfullAssetTransaction():
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5)
        blockchainTx = pw.waitFor(tx['id'])
        print(blockchainTx)
        assert blockchainTx['id'] == tx['id']

    def test_succesfullAssetTransactionWithAttachment():
        attachment = 'This is just a test...'
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, attachment = attachment)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_transactionFeeIsBiggerThanSelfBalance():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, feeAsset=myToken, txFee=100000000)
        assert str(error.value) == 'Insufficient Asset balance for fee'
    
    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)