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

def test_parallel_instances():
    """Test that two PyWaves instances can work independently"""
    # Create two separate instances
    pw1 = pw.PyWaves()
    pw2 = pw.PyWaves()
    
    # Configure them differently
    pw1.setNode('https://nodes.wavesnodes.com', 'W')
    pw2.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    
    # Verify they have independent state
    assert pw1.CHAIN == 'mainnet'
    assert pw1.CHAIN_ID == 'W'
    assert pw2.CHAIN == 'testnet'
    assert pw2.CHAIN_ID == 'T'
    assert pw1.NODE != pw2.NODE
    
    # Test that they can work independently
    height1 = pw1.height()
    height2 = pw2.height()
    
    # Both should return valid heights (positive numbers)
    assert isinstance(height1, int)
    assert isinstance(height2, int)
    assert height1 > 0
    assert height2 > 0
    
    print(f"Mainnet height: {height1}, Testnet height: {height2}")
