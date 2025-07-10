import pywaves as pw
from pywaves import address
import pytest
import os
from tests.helpers import Helpers
from pywaves import PyWavesException

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')
helpers = Helpers()

def test_generateNewTestnetAddress():
    addr = address.Address(seed = 'this is just a dummy test seed')
    assert addr.address.startswith('3N') or addr.address.startswith('3M') and addr.address != '3ND9vkY24sB1DFTETtbenEcpXdLdhtbhhtj'

def test_mainnetAddressCreationBySeed():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(seed = 'this is just a dummy test seed')

    assert addr.address.startswith('3P')

def test_mainnetAddressCreationByPublicKey():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(publicKey='H8PctYGqhsbbjgmJD5YgyMv6KuNXNAmZt3ho1Jym7Vir')

    assert addr.address.startswith('3PRAjhruvziPqhkeixrejgzdtWrQY1eUTjB')

def test_mainnetAddressCreationByAddress():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(address = '3PRAjhruvziPqhkeixrejgzdtWrQY1eUTjB')

    assert addr.address.startswith('3PRAjhruvziPqhkeixrejgzdtWrQY1eUTjB')

def test_mainnetAddressCreationWithInvalidAddress():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    with pytest.raises(PyWavesException) as error:
        address.Address(address = '3RAjhruvziPqhkeixrejgzdtWrQY1eUTjB')

    assert str(error.value) == 'Invalid address'


def test_mainnetAddressCreationWithEmptyPrivateKey():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    with pytest.raises(Exception) as error:
        address.Address()

    assert str(error.value) == 'Empty private key not allowed'

def test_testnetAddressCreationBySeed():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    addr = address.Address(seed='this is just a dummy test seed')

    assert addr.address.startswith('3N')

def test_stagenetAddressCreationBySeed():
    pw.setNode('https://nodes-stagenet.wavesnodes.com', 'S')
    addr = address.Address(seed='this is just a dummy test seed')

    assert addr.address.startswith('3M')

def test_mainnetWithAlias():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(alias = 'hawky')

    assert addr.address.startswith('3P')

def test_mainnetWithPrivateKey():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(privateKey = 'DQP9aFogWUJKGthnyERXU8jfVfp9CimCkGXVaMyyFyLM')

    assert addr.address.startswith('3P')

def test_mainnetWithNonce():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    addr = address.Address(seed = 'this is just a dummy test seed', nonce = 1)

    assert addr.address.startswith('3P')

def test_mainnetWithNegativeNonce():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    with pytest.raises(Exception) as error:
        address.Address(seed='this is just a dummy test seed', nonce=-5)

    assert str(error.value) == 'Nonce must be between 0 and 4294967295'

def test_mainnetWithHugeNonce():
    pw.setNode('https://nodes.wavesnodes.com', 'W')
    with pytest.raises(Exception) as error:
        address.Address(seed='this is just a dummy test seed', nonce=4294967297)

    assert str(error.value) == 'Nonce must be between 0 and 4294967295'

def test_resetNodetoTestnet():
    pw.setNode(PYWAVES_TEST_NODE, 'T')
    
