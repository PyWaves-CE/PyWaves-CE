from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
THISTEST = 'SendAsset'

pw.setThrowOnError(True)
pw.setNode(PYWAVES_TEST_NODE, 'T')

helpers = Helpers()
testwallet = helpers.prepareTestcase()
# pw_test_asset
myToken = asset.Asset('4Xq8bbfRV5R8NmKS9HyWepp3YcbqbzPHwe8wZcf9hn2z')

try:

    # no need to use testwallet, just use the address
    def test_assetTransactionWithoutPrivateKey():
        myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
        with pytest.raises(Exception) as error:
            myAddress.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 3)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_assetTransactionWithAmountSmallerEqualsZero():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, -1)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Amount must be > 0\') tblen=3>'

    def test_nonExistantAssetTransaction():
        myToken = asset.Asset('Test')
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 1)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Asset not issued\') tblen=3>'

    def test_assetTransactionButAmountBiggerThanBalance():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5000000000)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient asset balance\') tblen=3>'
   
    def test_transactionWithNoAsset():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), None, 100000000000000000)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient Waves balance\') tblen=3>'
  
    def test_successfulTransactionWithSponsoredFee():
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, feeAsset = myToken, txFee=1)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_succesfullAssetTransaction():
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5)
        blockchainTx = helpers.waitFor(tx['id'])
        print(blockchainTx)
        assert blockchainTx['id'] == tx['id']

    def test_succesfullAssetTransactionWithAttachment():
        attachment = 'This is just a test...'
        tx = testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, attachment = attachment)
        blockchainTx = helpers.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_transactionFeeIsBiggerThanSelfBalance():
        with pytest.raises(Exception) as error:
            testwallet.sendAsset(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), myToken, 5, feeAsset=myToken, txFee=100000000)
        assert str(error) == '<ExceptionInfo PyWavesException(\'Insufficient asset balance for fee\') tblen=3>'
    
    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)