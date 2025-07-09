from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os
import random
import string

helpers = Helpers()

try: 
    def test_prepareTestcase():
        global testwallet, address1, assetName
        testwallet = helpers.prepareTestcase(101000000)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)
        assetName = ''.join(random.choices(string.ascii_lowercase, k=8))

        assert testwallet is not None
        assert address1 is not None
        assert assetName is not None

    def test_issueSmartAssetWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            myAddress.issueSmartAsset(assetName, 'This is just a test smart asset', 10000000, scriptSource = script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_nameTooShort():
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            testwallet.issueSmartAsset('Sma', 'This is just a test smart asset', 10000000, scriptSource=script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Asset name must be between 4 and 16 characters long\') tblen=3>'

    def test_nameTooLong():
        script = 'match tx { \n' + \
                '  case _ => true\n' + \
                '}'
        with pytest.raises(Exception) as error:
            testwallet.issueSmartAsset('SmartTestAssetTeststst', 'This is just a test smart asset', 10000000, scriptSource=script)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Asset name must be between 4 and 16 characters long\') tblen=3>'

    def test_succesfullIssueSmartAsset():    
        script = 'match tx { \n' + \
                'case _ => true\n' + \
                '}'
        tx = testwallet.issueSmartAsset(assetName, 'This is just a test smart asset', 100, scriptSource=script, decimals=8, reissuable=True)
        pw.waitFor(tx['id'])
        print(tx)
        token = asset.Asset(tx['id'])
        
        assert token.status() == 'Issued'
        assert token.name == assetName.encode('ascii', 'ignore')
        assert token.description == "This is just a test smart asset".encode('ascii', 'ignore')
        assert token.quantity == 100
        assert token.decimals == 8
        assert token.reissuable == True

    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
