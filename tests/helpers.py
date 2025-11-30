import os
import pywaves as pw
import requests
import time
from pywaves import address
from pywaves import asset

PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')

class Helpers:

    def prepareTestcase(self, amount=1000000, sendTokens=False):
        pw.setNode(PYWAVES_TEST_NODE, 'T')
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        
        # generate a random address using 32 random bytes converted to base58
        seed = pw.b58encode(os.urandom(32))
        print(f"Using seed: {seed}")
        testwallet = address.Address(seed=seed)
        print(f"Operating on address: {testwallet.address}")
        
        testwalletBalance = testwallet.balance()
        # refill test wallet
       
        print(f"----- Sending waves to testwallet -----")
        tx = faucet.sendWaves(testwallet, amount)
        pw.waitFor(tx['id'])
        
        # check it faucet has test asset
        assets = faucet.assets()
        if (len(assets) == 0):
            tx = faucet.issueAsset('pw_testasset-3', f"Test Token", 10000000*(10**8), 8, reissuable=True)
            testtoken = asset.Asset(tx['id'])
            while not testtoken.status():
                pass
            # sponsor asset           
            assets = faucet.assets()        
            tx = faucet.sponsorAsset(assetId=assets[0], minimalFeeInAssets = 1000000)
            pw.waitFor(tx['id'])
        else:
            testtoken = asset.Asset(assets[0])
            

        # send some assets to testwallet
        if (sendTokens):
            print(f"----- Sending assets to testwallet -----")
            tx = faucet.sendAsset(testwallet, testtoken, 100000000)
            pw.waitFor(tx['id'])
        
        return testwallet

    def closeTestcase(self, testwallet):
        pw.setNode(PYWAVES_TEST_NODE, 'T')        
        faucet = address.Address(privateKey=PYWAVES_TEST_SECRET)
        # give time for the node to update the balance
        time.sleep(5)
        testwalletBalance = testwallet.balance()
        print(f"Testwallet balance: {testwalletBalance}")
    
        res = testwallet.script()
        #print(res)
        if (res['script'] != None):
            txFee = 400000+100000
        else:
            txFee = 100000
        amount = testwalletBalance-txFee
        print(f"Sending {amount} waves from {testwallet.address} back to faucet, txFee: {txFee}")
        if (amount > 0):
            print(f"Sending...")
            tx = testwallet.sendWaves(faucet, amount, txFee=txFee)
            #print(tx)
            pw.waitFor(tx['id'])


    