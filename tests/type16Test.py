from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest

pw.setThrowOnError(True)

def test_invokeScriptWithoutPrivateKey():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address('3MsZyHzDhSAVDcd7S1bHo6wgxcxvertc5GJ')
    scriptAcc = address.Address('3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm')
    parameter = [{"type": "integer", "value": 100, }, { "type": "string", "name": "test" }]

    with pytest.raises(Exception) as error:
        myAddress.invokeScript(scriptAcc, 'storeValue', parameter, [])

    assert str(error) == '<ExceptionInfo PyWavesException(\'Private key required\') tblen=3>'

# TODO: implement a proper example contract
def test_callToDefaultCallable():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3Myb6G8DkdBb8YcZzhrky65HrmiNuac3kvS' # Neutrino distribution contract in testnet

    tx = myAddress.invokeScript(scriptAcc, None)
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_acceptInvokeScriptWithStrAndInt():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [ { "type": "string", "value": "test" }, {"type": "integer", "value": 100, } ]

    tx = myAddress.invokeScript(scriptAcc, 'storeValue', parameter, [])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

#def test_acceptInvokeScriptWithBinary():
#    helpers = Helpers()
#   pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
#   myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
#   scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
#   parameter = [ { "type": "string", "value": "test" }, {"type": "binary", "value": "AFzTeKRwyomQ2wMtzBFriMzwJPG6HEJY3pbc8JrV6Z14" }]

#    tx = myAddress.invokeScript(scriptAcc, 'storeBinaryValue', parameter, [])
#    print(tx)
#    blockchainTx = helpers.waitFor(tx['id'])

#    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithBooleanTrue():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": True}]

    tx = myAddress.invokeScript(scriptAcc, 'storeBooleanValue', parameter, [])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithBooleanFalse():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": False}]

    tx = myAddress.invokeScript(scriptAcc, 'storeBooleanValue', parameter, [])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithListBooleanTrue():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [
        {"type": "string", "value": "Hello"},
        { "type": "list", "value": [ { "type": "string", "value": "test" } ] },
        { "type": "list", "value": [ { "type": "integer", "value":  100 } ] },
        { "type": "list", "value": [ { "type": "boolean", "value": True } ] }
    ]

    tx = myAddress.invokeScript(scriptAcc, 'storeListValue', parameter, [ ])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithAssetPayment():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": True}]

    tx = myAddress.invokeScript(scriptAcc, 'storeBooleanValue', parameter, [{'amount': 10, 'assetId': '5Cs2APZPHeXqhB2At2qWT2wUuCe9SjxitFYdXhj6Q8FL'}])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithListBooleanFalse():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [
        {"type": "string", "value": "Hello"},
        { "type": "list", "value": [ { "type": "string", "value": "test" } ] },
        { "type": "list", "value": [ { "type": "integer", "value":  100 } ] },
        { "type": "list", "value": [ { "type": "boolean", "value": False } ] }
    ]

    tx = myAddress.invokeScript(scriptAcc, 'storeListValue', parameter, [])
    blockchainTx = helpers.waitFor(tx['id'])

    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithWavesPayment():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": True}]

    tx = myAddress.invokeScript(scriptAcc, 'storeBooleanValue', parameter, [{'amount': 10, 'assetId': '' }] )
    blockchainTx = helpers.waitFor(tx['id'])
    assert blockchainTx['id'] == tx['id']

def test_invokeScriptWithFeeAsset():
    helpers = Helpers()
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": True}]

    tx = myAddress.invokeScript(scriptAcc, 'storeBooleanValue', parameter, [{'amount': 10, 'assetId': '3GNGfcfPbJCQMoSCULtaa2xQpDgDMrxeUwgnKDtkzPbq' }], txFee=5, feeAsset='7oSYZxQUvB8aKqPQupqQt2b5nipegxkR1vszFQVH6Gjg' )
    print(tx)
    blockchainTx = helpers.waitFor(tx['id'])
    assert blockchainTx['id'] == tx['id']

def test_invokeButPywavesOffline():
    pw.setNode('https://nodes-testnet.wavesnodes.com', 'T')
    myAddress = address.Address(privateKey='BGpBRDeUiHskf4bdyWoUAKpP9DSx51haovHcGNqPEy6Q')
    scriptAcc = '3MwGH6GPcq7jiGNXgS4K6buynpLZR5LAgQm'
    parameter = [{"type": "string", "value": "test"},
                 {"type": "boolean", "value": True}]

    pw.setOffline()
    tx = myAddress.invokeScript(scriptAcc,'storeBooleanValue', parameter, [])
    pw.setOnline()

    assert tx['api-type'] == 'POST'
