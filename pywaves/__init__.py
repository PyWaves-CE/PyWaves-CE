# Copyright (C) 2017 PyWaves Developers
#
# This file is part of PyWaves.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import requests
import base58
import pywaves.crypto as crypto
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logging.getLogger("pywaves").setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

# Constants
DEFAULT_TX_FEE = 100000
DEFAULT_BASE_FEE = DEFAULT_TX_FEE
DEFAULT_SMART_FEE = 400000
DEFAULT_ASSET_FEE = 100000000
DEFAULT_MATCHER_FEE = 1000000
DEFAULT_LEASE_FEE = 100000
DEFAULT_ALIAS_FEE = 100000
DEFAULT_SPONSOR_FEE = 100000000
DEFAULT_SCRIPT_FEE = 100000
DEFAULT_ASSET_SCRIPT_FEE = 100000000
DEFAULT_SET_SCRIPT_FEE = 1000000
DEFAULT_INVOKE_SCRIPT_FEE = 500000
DEFAULT_CURRENCY = 'WAVES'
VALID_TIMEFRAMES = (5, 15, 30, 60, 240, 1440)
MAX_WDF_REQUEST = 100

# Address constants
ADDRESS_VERSION = 1
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

class PyWavesException(Exception):
    def __init__(self, msg):
        self.msg = msg
        logging.error("An exception occurred: " + msg)
        super().__init__(msg)

class PyWaves(object):
    """Main class for working with Waves blockchain"""
    def __init__(self):
        # State (instance-specific)
        self.OFFLINE = False
        self.NODE = None
        self.CHAIN = 'mainnet'
        self.CHAIN_ID = 'W'
        self.MATCHER = None
        self.MATCHER_PUBLICKEY = None
        self.DATAFEED = None

    def throwException(self, msg):
        raise PyWavesException(msg)

    def setOffline(self):
        self.OFFLINE = True

    def setOnline(self):
        self.OFFLINE = False

    def setChain(self, chain = None, chain_id = None):
        if chain is None:
            chain = self.CHAIN
        if chain_id is not None:
            self.CHAIN = chain
            self.CHAIN_ID = chain_id
        else:
            if chain.lower()=='mainnet' or chain.lower()=='w':
                self.CHAIN = 'mainnet'
                self.CHAIN_ID = 'W'
            elif chain.lower()=='hacknet' or chain.lower()=='u':
                self.CHAIN = 'hacknet'
                self.CHAIN_ID = 'U'
            elif chain.lower()=='stagenet' or chain.lower()=='s':
                self.CHAIN = 'stagenet'
                self.CHAIN_ID = 'S'
            else:
                self.CHAIN = 'testnet'
                self.CHAIN_ID = 'T'

    def getChain(self):
        return self.CHAIN

    def setNode(self, node = None, chain = None, chain_id = None):
        if node is None:
            node = 'https://nodes.wavesnodes.com'
        self.NODE = node.rstrip("/")
        self.setChain(chain, chain_id)

    def getNode(self):
        return self.NODE

    def setMatcher(self, node=None):
        if node is None:
            node = 'https://matcher.waves.exchange'
        node = node.rstrip("/")
        self.MATCHER = node
        try:
            self.MATCHER_PUBLICKEY = self.wrapper('/matcher', host=node)
            logging.info('Setting matcher %s %s' % (self.MATCHER, self.MATCHER_PUBLICKEY))
        except:
            self.MATCHER_PUBLICKEY = ''

    def setDatafeed(self, node=None):
        if node is None:
            node = 'https://api.wavesplatform.com'
        self.DATAFEED = node.rstrip("/")
        logging.info('Setting datafeed %s ' % (self.DATAFEED))

    def getDatafeed(self):
        return self.DATAFEED

    def _format_json_decode_error(self, response, url, e):
        api_error = {
            'error': 1,  # WrongJson
            'message': f"Failed to decode JSON: {str(e)}"
        }
        if response.text:
            api_error['response'] = response.text
        elif response.content:
            api_error['response'] = response.content
        else:
            api_error['response'] = None
        return api_error

    def wrapper(self, api, postData='', host='', headers=''):
        if self.OFFLINE:
            offlineTx = {}
            offlineTx['api-type'] = 'POST' if postData else 'GET'
            offlineTx['api-endpoint'] = api
            offlineTx['api-data'] = postData
            return offlineTx
        if not host:
            host = self.NODE
        if postData:
            url = '%s%s' % (host, api)
            response = requests.post(url, data=postData, headers={'content-type': 'application/json'})
        else:
            url = '%s%s' % (host, api)
            response = requests.get(url, headers=headers)

        if response.status_code >= 400:
            api_error = {
                'error': response.status_code,
                'message': f"HTTP {response.status_code}"
            }
            try:
                error_response = response.json()
                if isinstance(error_response, dict) and 'error' in error_response and 'message' in error_response:
                    api_error = error_response
                else:
                    api_error['response'] = error_response
                    api_error['message'] = f"HTTP {response.status_code}: {str(error_response)[:200]}"
            except ValueError as e:
                api_error = self._format_json_decode_error(response, url, e)
                logging.error(f"[wrapper] {url} -> {api_error['error']} ({api_error['message']})")
                return api_error
            # 311 (TransactionDoesNotExist) expected during waitFor() polling
            if api_error.get('error') == 311:
                logging.debug(f"[wrapper] {url} -> {api_error['error']} ({api_error['message']})")
            else:
                logging.warning(f"[wrapper] {url} -> {api_error['error']} ({api_error['message']})")
            return api_error

        try:
            return response.json()
        except ValueError as e:
            api_error = self._format_json_decode_error(response, url, e)
            logging.error(f"[wrapper] {url} -> {api_error['error']} ({api_error['message']})")
            return api_error

    def height(self):
        return self.wrapper('/blocks/height')['height']

    def lastblock(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        return self.wrapper('/transactions/info/%s' % id)

    def stateChangeForTx(self, id):
        return self.wrapper('/debug/stateChanges/info/' + id)

    def stateChangesForAddress(self, address, limit = 1000):
        return self.wrapper('/debug/stateChanges/address/' + address + '/limit/' + str(limit))

    def getOrderBook(self, assetPair):
        orderBook = assetPair.orderbook()
        try:
            bids = orderBook['bids']
            asks = orderBook['asks']
        except:
            bids = ''
            asks = ''
        return bids, asks

    def markets(self):
        return self.wrapper('/matcher/orderbook', host=self.MATCHER)

    def validateAddress(self, address):
        addr = crypto.bytes2str(self.b58decode(address))
        if addr[0] != chr(ADDRESS_VERSION):
            logging.error("Wrong address version")
        elif addr[1] != self.CHAIN_ID:
            logging.error("Wrong chain id")
        elif len(addr) != ADDRESS_LENGTH:
            logging.error("Wrong address length")
        elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
            logging.error("Wrong address checksum")
        else:
            return True
        return False

    def b58encode(self, data):
        result = base58.b58encode(data)
        if isinstance(result, bytes):
            return result.decode('utf-8')
        return result

    def b58decode(self, data):
        return base58.b58decode(data)

    def waitFor(self, id, timeout=30, hard_timeout=False):
        n = 0
        n_utx = 0
        first = True

        while True:

            if first:
                first = False
            else:
                time.sleep(1)
                n += 1

            try:
                tx_data = self.tx(id)
            except:
                tx_data = None

            if tx_data and 'error' not in tx_data:
                if tx_data['applicationStatus'] == 'succeeded':
                    logging.info(f"Transaction {id} confirmed")
                else:
                    logging.error(f"Transaction {id} failed with status: {tx_data['applicationStatus']}")
                return tx_data

            if hard_timeout and n >= timeout:
                logging.warning(f"Transaction {id} hard timeout reached")
                raise TimeoutError(f"Transaction {id} hard timeout reached")

            if n_utx:
                n_diff = n - n_utx
                if n_diff > timeout:
                    try:
                        unconfirmed = self.wrapper('/transactions/unconfirmed/info/' + id)
                    except:
                        unconfirmed = None

                    if unconfirmed and 'error' not in unconfirmed:
                        logging.warning(f"Transaction {id} found in unconfirmed again ({n})")
                        n_utx = 0
                        continue

                    logging.error(f"Transaction {id} not found (timeout reached)")
                    raise TimeoutError(f"Transaction {id} not found (timeout reached)")

                if n_diff >= 1:
                    logging.info(f"Transaction {id} still unconfirmed ({n}) (timeout {n_diff}/{timeout})")

            else:
                try:
                    unconfirmed = self.wrapper('/transactions/unconfirmed/info/' + id)
                except:
                    unconfirmed = None

                if unconfirmed and 'error' not in unconfirmed:
                    logging.info(f"Transaction {id} unconfirmed" + (f" ({n})" if n > 0 else ""))
                    continue

                n_utx = n

    def isWavesBalanceEnough(self, address_obj, amount):
        if not self.OFFLINE and address_obj.balance() < amount:
            raise PyWavesException('Insufficient Waves balance')

    def isAssetBalanceEnough(self, address_obj, asset, amount):
        if not self.OFFLINE and asset is not None and address_obj.balance(asset.assetId) < amount:
            raise PyWavesException('Insufficient Asset balance')

    def requirePrivateKey(self, address_obj):
        if not address_obj.privateKey:
            raise PyWavesException('Private key required')

    def amountMustBePositive(self, amount):
        if amount <= 0:
            raise PyWavesException('Amount must be > 0')

    def assetMustBeIssued(self, address_obj, asset):
        if not self.OFFLINE and asset and not asset.status():
            raise PyWavesException('Asset not issued')

    def timefraneMustBeValid(self, timeframe):
        if timeframe not in VALID_TIMEFRAMES:
            raise PyWavesException('Invalid timeframe')

    def assetNameMustBeValid(self, name):
        if len(name) < 4 or len(name) > 16:
            raise PyWavesException('Asset name must be between 4 and 16 characters long')

    def tooManyRecipientsForMassTransfer(self, recipients):
        if len(recipients) > 100:
            raise PyWavesException('Too many recipients')

_pw_instance = PyWaves()
pw = _pw_instance

from .address import *
from .asset import *
from .order import *
from .contract import *
from .oracle import *
from .WXFeeCalculator import *
from .txGenerator import *
from .txSigner import *

ParallelPyWaves = PyWaves

def throwException(msg):
    return _pw_instance.throwException(msg)

def setOffline():
    _pw_instance.setOffline()

def setOnline():
    _pw_instance.setOnline()

def setChain(chain = None, chain_id = None):
    _pw_instance.setChain(chain, chain_id)

def getChain():
    return _pw_instance.getChain()

def setNode(node = None, chain = None, chain_id = None):
    _pw_instance.setNode(node, chain, chain_id)

def getNode():
    return _pw_instance.getNode()

def setMatcher(node=None):
    _pw_instance.setMatcher(node)

def setDatafeed(node=None):
    _pw_instance.setDatafeed(node)

def getDatafeed():
    return _pw_instance.getDatafeed()

def wrapper(api, postData='', host='', headers=''):
    return _pw_instance.wrapper(api, postData, host, headers)

def height():
    return _pw_instance.height()

def lastblock():
    return _pw_instance.lastblock()

def block(n):
    return _pw_instance.block(n)

def tx(id):
    return _pw_instance.tx(id)

def stateChangeForTx(id):
    return _pw_instance.stateChangeForTx(id)

def stateChangesForAddress(address, limit = 1000):
    return _pw_instance.stateChangesForAddress(address, limit)

def getOrderBook(assetPair):
    return _pw_instance.getOrderBook(assetPair)

def markets():
    return _pw_instance.markets()

def validateAddress(address):
    return _pw_instance.validateAddress(address)

def b58encode(data):
    return _pw_instance.b58encode(data)

def b58decode(data):
    return _pw_instance.b58decode(data)

def waitFor(id, timeout=30, hard_timeout=False):
    return _pw_instance.waitFor(id, timeout, hard_timeout)

def __getattr__(name):
    """Delegates module attribute access to PyWaves instance"""
    if hasattr(_pw_instance, name):
        return getattr(_pw_instance, name)
    raise AttributeError(f"module 'pywaves' has no attribute '{name}'")
