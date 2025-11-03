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

THROW_EXCEPTION_ON_ERROR = False

import requests
import base58
import pywaves.crypto as crypto
import time
import logging

from .address import *
from .asset import *
from .order import *
from .contract import *
from .oracle import *
from .ParallelPyWaves import *
from .WXFeeCalculator import *
from .txGenerator import *
from .txSigner import *

OFFLINE = False
NODE = 'https://nodes.wavesnodes.com'

ADDRESS_VERSION = 1
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

CHAIN = 'mainnet'
CHAIN_ID = 'W'
#MATCHER = 'https://nodes.wavesnodes.com'
#MATCHER = 'http://matcher.wavesnodes.com'
MATCHER = 'https://matcher.waves.exchange'
#MATCHER_PUBLICKEY = ''
MATCHER_PUBLICKEY = '9cpfKN9suPNvfeUNphzxXMjcnn974eme8ZhWUjaktzU5'

#DATAFEED = 'http://marketdata.wavesplatform.com'
DATAFEED = 'https://api.wavesplatform.com'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logging.getLogger("pywaves").setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


class PyWavesException(ValueError):
    pass


def throw_error(msg):
    if THROW_EXCEPTION_ON_ERROR:
        raise PyWavesException(msg)


def setThrowOnError(throw=True):
    global THROW_EXCEPTION_ON_ERROR
    THROW_EXCEPTION_ON_ERROR = throw


def setOffline():
    global OFFLINE
    OFFLINE = True

def setOnline():
    global OFFLINE
    OFFLINE = False

def setChain(chain = CHAIN, chain_id = None):
    global CHAIN, CHAIN_ID

    if chain_id is not None:
        CHAIN = chain
        CHAIN_ID = chain_id
    else:
        if chain.lower()=='mainnet' or chain.lower()=='w':
            CHAIN = 'mainnet'
            CHAIN_ID = 'W'
        elif chain.lower()=='hacknet' or chain.lower()=='u':
            CHAIN = 'hacknet'
            CHAIN_ID = 'U'
        elif chain.lower()=='stagenet' or chain.lower()=='s':
            CHAIN = 'stagenet'
            CHAIN_ID = 'S'
        else:
            CHAIN = 'testnet'
            CHAIN_ID = 'T'

def getChain():
    return CHAIN

def setNode(node = NODE, chain = CHAIN, chain_id = None):
    global NODE, CHAIN, CHAIN_ID
    NODE = node.rstrip("/")
    setChain(chain, chain_id)

def getNode():
    return NODE

def setMatcher(node = MATCHER):
    global MATCHER, MATCHER_PUBLICKEY
    try:
        MATCHER_PUBLICKEY = wrapper('/matcher', host = node)
        MATCHER = node
        logging.info('Setting matcher %s %s' % (MATCHER, MATCHER_PUBLICKEY))
    except:
        MATCHER_PUBLICKEY = ''

def setDatafeed(wdf = DATAFEED):
    global DATAFEED
    DATAFEED = wdf
    logging.info('Setting datafeed %s ' % (DATAFEED))

def _format_json_decode_error(response, url, e):
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

def wrapper(api, postData='', host='', headers=''):
    global OFFLINE
    if OFFLINE:
        offlineTx = {}
        offlineTx['api-type'] = 'POST' if postData else 'GET'
        offlineTx['api-endpoint'] = api
        offlineTx['api-data'] = postData
        return offlineTx
    if not host:
        host = NODE
    if postData:
        url = '%s%s' % (host, api)
        #print(f"Making POST request to: {url}")
        response = requests.post(url, data=postData, headers={'content-type': 'application/json'})
    else:
        url = '%s%s' % (host, api)
        #print(f"Making GET request to: {url}")
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
            api_error = _format_json_decode_error(response, url, e)
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
        api_error = _format_json_decode_error(response, url, e)
        logging.error(f"[wrapper] {url} -> {api_error['error']} ({api_error['message']})")
        return api_error

def height():
    return wrapper('/blocks/height')['height']

def lastblock():
    return wrapper('/blocks/last')

def block(n):
    return wrapper('/blocks/at/%d' % n)

def tx(id):
    return wrapper('/transactions/info/%s' % id)

def stateChangeForTx(id):
    return wrapper('/debug/stateChanges/info/' + id)

def stateChangesForAddress(address, limit = 1000):
    return wrapper('/debug/stateChanges/address/' + address + '/limit/' + str(limit))

def getOrderBook(assetPair):
    orderBook = assetPair.orderbook()
    try:
        bids = orderBook['bids']
        asks = orderBook['asks']
    except:
        bids = ''
        asks = ''
    return bids, asks


# Deprecated due to the removal of the endpoint
# def symbols(self):
#    return self.wrapper('/api/symbols', host=DATAFEED)

def markets(self):
    return self.wrapper('/matcher/orderbook', host=MATCHER)
    # return self.wrapper('/api/markets', host=DATAFEED)

def validateAddress(address):
    addr = crypto.bytes2str(b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != CHAIN_ID:
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False
def b58encode(data):
    return base58.b58encode(data).decode('utf-8')

def b58decode(data):
    return base58.b58decode(data)

def waitFor(id, timeout=30, hard_timeout=False):
    n = 0
    n_utx = 0
    first = True
        
    while True:

        if first:
            first = False
        else:
            time.sleep(1)
            n += 1
            n_diff = n - n_utx

        try:
            tx_data = tx(id)
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
                    unconfirmed = wrapper('/transactions/unconfirmed/info/' + id)
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
                unconfirmed = wrapper('/transactions/unconfirmed/info/' + id)
            except:
                unconfirmed = None

            if unconfirmed and 'error' not in unconfirmed:
                logging.info(f"Transaction {id} unconfirmed" + (f" ({n})" if n > 0 else ""))
                continue

            n_utx = n
