from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os  


helpers = Helpers()


try:

    def test_prepareTestcase():
        global testwallet, address1, dappaddress1, myToken
        testwallet = helpers.prepareTestcase(100000000, sendTokens=True)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)

        seed = pw.b58encode(os.urandom(32))
        dappaddress1 = address.Address(seed=seed)

        # fund dappaddress1
        tx = testwallet.sendWaves(dappaddress1, 1000000)
        pw.waitFor(tx['id'])

        assets = testwallet.assets()
        myToken = assets[0]

        assert testwallet is not None
        assert address1 is not None
        assert dappaddress1 is not None
        assert myToken is not None

    def test_invokeScriptWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        parameters = [{"type": "integer", "value": 100, }, { "type": "string", "name": "test" }]

        with pytest.raises(Exception) as error:
            myAddress.invokeScript(dappaddress1.address, 'storeValue', parameters, [])

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

    def test_callToDefaultCallable():      
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
        
        tx = dappaddress1.setScript(script, txFee=500000)
        blockchainTx = pw.waitFor(tx['id'])

        tx = testwallet.invokeScript(dappaddress1.address, None)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_setScript():
        script ='{-# STDLIB_VERSION 5 #-}\n' \
            '{-# CONTENT_TYPE DAPP #-}\n' \
            '{-# SCRIPT_TYPE ACCOUNT #-}\n' \
            '\n' \
            '@Callable(i)\n' \
            'func storeValue(name: String, value: Int) = {\n' \
            '[ IntegerEntry(name, value) ]\n' \
            '}\n' \
            '\n' \
            '@Verifier(tx)\n' \
            'func verify() = sigVerify(tx.bodyBytes, tx.proofs[0], tx.senderPublicKey)\n' \
            '\n' \
            '@Callable(i)\n' \
            'func storeListValue(name: String, value1: List[String], value2: List[Int], value3: List[Boolean]) = {\n' \
            '[\n' \
            'StringEntry(name + "_0", value1[0]),\n' \
            'IntegerEntry(name + "_1", value2[0]),\n' \
            'BooleanEntry(name + "_2", value3[0]) ]\n' \
            '}\n' \
            '\n' \
            '@Callable(i)\n' \
            'func storeBinaryValue(name: String, value: ByteVector) = {\n' \
            '[BinaryEntry(name, value)]\n' \
            '}\n' \
            '\n' \
            '@Callable(i)\n' \
            'func storeBooleanValue(name: String, value: Boolean) = {\n' \
            '[BooleanEntry(name, value)]\n' \
            '}'

        tx = dappaddress1.setScript(script, txFee=500000)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']    

    def test_acceptInvokeScriptWithStrAndInt():
        
        parameters = [ { "type": "string", "value": "test" }, {"type": "integer", "value": 100, } ]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeValue', parameters, [])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithBooleanTrue():
        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": True}]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeBooleanValue', parameters, [])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithBooleanFalse():       
        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": False}]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeBooleanValue', parameters, [])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithListBooleanTrue():

        parameters = [
            {"type": "string", "value": "Hello"},
            { "type": "list", "value": [ { "type": "string", "value": "test" } ] },
            { "type": "list", "value": [ { "type": "integer", "value":  100 } ] },
            { "type": "list", "value": [ { "type": "boolean", "value": True } ] }
        ]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeListValue', parameters, [ ])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithAssetPayment():

        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": True}]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeBooleanValue', parameters, [{'amount': 10, 'assetId': myToken}])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithListBooleanFalse():
        parameters = [
            {"type": "string", "value": "Hello"},
            { "type": "list", "value": [ { "type": "string", "value": "test" } ] },
            { "type": "list", "value": [ { "type": "integer", "value":  100 } ] },
            { "type": "list", "value": [ { "type": "boolean", "value": False } ] }
        ]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeListValue', parameters, [])
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithWavesPayment():
        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": True}]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeBooleanValue', parameters, [{'amount': 10, 'assetId': '' }] )
        blockchainTx = pw.waitFor(tx['id'])
        assert blockchainTx['id'] == tx['id']

    def test_invokeScriptWithFeeAsset():
        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": True}]

        tx = testwallet.invokeScript(dappaddress1.address, 'storeBooleanValue', parameters, [{'amount': 10, 'assetId': myToken}], txFee=5000000, feeAsset=myToken )
        print(tx)
        blockchainTx = pw.waitFor(tx['id'])
        assert blockchainTx['id'] == tx['id']

    def test_invokeButPywavesOffline():
        parameters = [{"type": "string", "value": "test"},
                    {"type": "boolean", "value": True}]
        pw.setOffline()
        tx = testwallet.invokeScript(dappaddress1.address,'storeBooleanValue', parameters, [])
        pw.setOnline()

        assert tx['api-type'] == 'POST'

    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)


