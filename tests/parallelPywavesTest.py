from tests.helpers import Helpers
import pywaves as pw
from pywaves import address

def test_successfulTransfer():
    helpers = Helpers()
    parallelPW = pw.ParallelPyWaves()
    parallelPW.setNode('https://nodes-testnet.wavesnodes.com', 'T')

    myAddress = address.Address(privateKey= 'BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q', pywaves=parallelPW)

    tx = myAddress.sendWaves(address.Address('3MuqNWyf4RMWz3cqDi4QZRVr9v76LKMjNVZ', pywaves=parallelPW), 1*10*4, txFee=500000)
    blockchainTx = pw.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']
