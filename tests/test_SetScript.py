from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os

pw.setThrowOnError(True)
helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet, address1
        testwallet = helpers.prepareTestcase(1500000)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)
        assert testwallet is not None
        assert address1 is not None

    def test_setScriptWithoutPrivateKey():
        myAddress = address.Address(address1.address)
        scriptSource =  '{-# STDLIB_VERSION 5 #-}\n' \
                        '{-# CONTENT_TYPE DAPP #-}\n' \
                        '{-# SCRIPT_TYPE ACCOUNT #-}\n'\
                        '\n' \
                        '@Callable(i)\n' \
                        'func storeValue(name: String, value: Int) = {\n'\
                        '[ IntegerEntry(name, value) ]\n'\
                        '}\n'\
                        '\n'\
                        '@Verifier(tx)\n'\
                        'func verify() = sigVerify(tx.bodyBytes, tx.proofs[0], tx.senderPublicKey)'


        with pytest.raises(Exception) as error:
            myAddress.setScript(scriptSource)

        assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=4>'

    def test_succesfullSetScript():
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

        tx = testwallet.setScript(script, txFee=500000)
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
