import pywaves as pw
from pywaves import address
import pytest
import os
import json
from pywaves.txSigner import TxSigner
from pywaves.txGenerator import TxGenerator
from tests.helpers import Helpers
from pywaves import PyWavesException

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()

try:

    def test_prepareTestcase():
        global testwallet 
        testwallet = helpers.prepareTestcase(10000000)        
        assert testwallet is not None        

    def test_validateTX_valid():
        txgenerator = TxGenerator()
        signer = TxSigner()
        tx = txgenerator.generateSendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100000, testwallet.publicKey)    
        signer.signTx(tx, testwallet.privateKey)
        print (json.dumps(tx, indent=4))
        v = pw.validateTx(json.dumps(tx))
        assert v['valid'] == True

    def test_validateTX_invalid():
        txgenerator = TxGenerator()
        signer = TxSigner()
        tx = txgenerator.generateSendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100000, testwallet.publicKey)    
        tx['timestamp'] = tx['timestamp'] - 1000000000000
        signer.signTx(tx, testwallet.privateKey)
        #print (json.dumps(tx, indent=4))
        v = pw.validateTx(json.dumps(tx))
        assert v['valid'] == False        
    
    def test_evaluateScript():
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
        
        txgenerator = TxGenerator()
        parameters = [{"type": "string", "value": "test"},
            {"type": "boolean", "value": True}]

        tx = txgenerator.generateInvokeScript(
            testwallet.address,
            'storeBooleanValue',
            testwallet.publicKey,
            parameters,
            [],
            None,
            txFee=5000000
        )
        v = pw.evaluateScript(testwallet.address, json.dumps(tx))
        assert v.get('complexity', None) == 2
        

    def test_closeTestcase():
        print('----- Closing testcase -----')
        helpers.closeTestcase(testwallet)

except Exception as e:
    print('Exception: ', e)
    print('----- Closing testcase due to exception -----')
    helpers.closeTestcase(testwallet)    