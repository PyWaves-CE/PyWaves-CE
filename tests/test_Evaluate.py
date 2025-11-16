import pywaves as pw
from pywaves import address
import pytest
import os
import json
from pywaves.txGenerator import TxGenerator
from pywaves.txSigner import TxSigner
from tests.helpers import Helpers
from pywaves import PyWavesException

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()

try:

    def test_prepareTestcase():
        global testwallet 
        testwallet = helpers.prepareTestcase()        
        assert testwallet is not None        

    def test_validateTX_valid():
        generator = TxGenerator()        
        signer = TxSigner()
        tx = generator.generateSendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100000, testwallet.publicKey)    
        signer.signTx(tx, testwallet.privateKey)
        print (json.dumps(tx, indent=4))
        v = generator.validateTx(json.dumps(tx))
        assert v['valid'] == True

    def test_validateTX_invalid():
        generator = TxGenerator()        
        signer = TxSigner()
        tx = generator.generateSendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ'), 100000, testwallet.publicKey)    
        tx['timestamp'] = tx['timestamp'] - 1000000000000
        signer.signTx(tx, testwallet.privateKey)
        #print (json.dumps(tx, indent=4))
        v = generator.validateTx(json.dumps(tx))
        assert v['valid'] == False        

    def test_closeTestcase():
        print('----- Closing testcase -----')
        helpers.closeTestcase(testwallet)

except Exception as e:
    print('Exception: ', e)
    print('----- Closing testcase due to exception -----')
    helpers.closeTestcase(testwallet)    