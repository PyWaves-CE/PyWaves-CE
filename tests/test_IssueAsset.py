import pywaves as pw
from pywaves import address
from pywaves import asset
import time
from tests.helpers import Helpers
import os
import pytest


NAME = 'Issue' + time.strftime('%y%m%d')
helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet
        testwallet = helpers.prepareTestcase(101000000)
        assert testwallet is not None

    def test_issueAssetWithoutPrivateKey():
        with pytest.raises(Exception) as error:
            myAddress = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
            tx = myAddress.issueAsset('Test2','This is just another test asset', 100000, 1)

        assert str(error.value) == 'Private key required'

    def test_issueAssetWithTooShortName():
        with pytest.raises(Exception) as error:
            tx = testwallet.issueAsset('Tes','This is just another test asset', 100000, 1)

        assert str(error.value) == 'Asset name must be between 4 and 16 characters long'

    def test_pywavesOffline():
        pw.setOffline()
        tx = testwallet.issueAsset('Test2', 'this is just another test asset', 10000, 0)
        pw.setOnline()

        assert tx['api-type'] == 'POST'

    def test_issueAssetWithTooLongName():
        with pytest.raises(Exception) as error:
            tx = testwallet.issueAsset('12345678912345678','This is just another test asset', 100000, 1)

        assert str(error.value) == 'Asset name must be between 4 and 16 characters long'

    def test_successfulIssueAsset():
        tx = testwallet.issueAsset(NAME, f"Test Token {NAME}", 100, 8, reissuable=True)
        pw.waitFor(tx['id'])
        token = asset.Asset(tx['id'])
        
        assert token.status() == 'Issued'
        assert token.name == NAME.encode('ascii', 'ignore')
        assert token.description == f"Test Token {NAME}".encode('ascii', 'ignore')
        assert token.quantity == 100
        assert token.decimals == 8
        assert token.reissuable == True

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
