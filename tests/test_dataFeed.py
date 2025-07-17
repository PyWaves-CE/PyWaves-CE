from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
import pytest
import os  

helpers = Helpers()
PYWAVES_TEST_SECRET = os.getenv('PYWAVES_TEST_SECRET')
PYWAVES_TEST_NODE = os.getenv('PYWAVES_TEST_NODE')
pw.setNode(PYWAVES_TEST_NODE, 'T')


try:

    def test_dataFeed():

        pw.setDatafeed('https://api.wavesplatform.com')
        data = pw.wrapper('/v0/assets/GjwAHMjqWzYR4LgoNy91CxUKAGJN79h2hseZoae4nU8t', host = pw.getDatafeed())
        print(data)
        assert data['data']['name'] == 'UNIT0'
        #TODO: make tests in testnet

except Exception as e:
    print("Exception: ", e)
    print("----- Closing testcase due to exception -----")
    helpers.closeTestcase(testwallet)


