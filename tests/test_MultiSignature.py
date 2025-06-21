from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pywaves.crypto as crypto
from pywaves.txSigner import TxSigner
from pywaves.txGenerator import TxGenerator
import os

pw.setThrowOnError(True)
helpers = Helpers()

try:
    def test_prepareTestcase():
        global testwallet, multisigAddress, address1, address2
        testwallet = helpers.prepareTestcase(200000000)
        seed = pw.b58encode(os.urandom(32))
        multisigAddress = address.Address(seed=seed)
        seed = pw.b58encode(os.urandom(32))
        address1 = address.Address(seed=seed)
        seed = pw.b58encode(os.urandom(32))
        address2 = address.Address(seed=seed)

        assert testwallet is not None
        assert multisigAddress is not None
        assert address1 is not None
        assert address2 is not None

    def test_createMultiSignatureAddress():

        script = '{-# STDLIB_VERSION 5 #-}\n' \
        '{-# SCRIPT_TYPE ACCOUNT #-}\n' \
        '{-# CONTENT_TYPE DAPP  #-}\n' \
        'let publicKey1 = base58\'' + testwallet.publicKey + '\'\n' \
        'let publicKey2 = base58\'' + address1.publicKey + '\'\n' \
        'let publicKey3 = base58\'' + address2.publicKey + '\'\n' \
        'let threshold = 2\n' \
        '@Verifier(tx)\n' \
        'func verify() = {\n' \
        '    let sig1Valid = if tx.proofs.size() > 0 then sigVerify(tx.bodyBytes, tx.proofs[0], publicKey1) else false\n' \
        '    let sig2Valid = if tx.proofs.size() > 1 then sigVerify(tx.bodyBytes, tx.proofs[1], publicKey2) else false\n' \
        '    let sig3Valid = if tx.proofs.size() > 2 then sigVerify(tx.bodyBytes, tx.proofs[2], publicKey3) else false\n' \
        '    let sig1Count = if sig1Valid then 1 else 0\n' \
        '    let sig2Count = if sig2Valid then 1 else 0\n' \
        '    let sig3Count = if sig3Valid then 1 else 0\n' \
        '    sig1Count + sig2Count + sig3Count >= threshold\n' \
        '}'

        # fund multisig address

        tx = testwallet.sendWaves(multisigAddress, 100000000)
        pw.waitFor(tx['id'])
        
        tx = multisigAddress.setScript(script, txFee=500000)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']
        
    def test_sendWaves():
        generator = TxGenerator()
        signer = TxSigner()
        # Send FROM multisig address TO address2
        tx = generator.generateSendWaves(testwallet, 1, multisigAddress.publicKey, txFee=500000)
        print(tx)
        
        # Sign with two different keys to meet the threshold requirement
        signer.signTx(tx, testwallet.privateKey)
        signer.signTx(tx, address1.privateKey)

        tx = multisigAddress.broadcastTx(tx)
        print(tx)
        blockchainTx = pw.waitFor(tx['id'])

        assert blockchainTx['id'] == tx['id']

    '''
    def test_sendWavesWithAttachment():
        helpers = Helpers()
        pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
        firstAddress = address.Address(seed = 'this is just a simple test seed one')
        secondAddress = address.Address(seed = 'this is just a simple test seed two')
        attachment = 'just a test transfer'

        generator = TxGenerator()
        signer = TxSigner()
        tx = generator.generateSendWaves(secondAddress, 1, firstAddress.publicKey, attachment = attachment, txFee=500000)
        signer.signTx(tx, firstAddress.privateKey)
        signer.signTx(tx, secondAddress.privateKey)

        res = firstAddress.broadcastTx(tx)
        blockchainTx = pw.waitFor(res['id'])

        assert blockchainTx['id'] == res['id']
'''
    # Dummy test case to return funds to faucet
    def test_closeTestcase():
        print("----- Closing testcase -----")
        helpers.closeTestcase(testwallet)

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)
