from tests.helpers import Helpers
import pywaves as pw
from pywaves import address
from pywaves import asset
from pywaves.WXFeeCalculator import WXFeeCalculator
import requests

pw.setMatcher('https://matcher.waves.exchange')

def test_getCalculatePercentDiscountedBuyingFee():
    pw.setMatcher('https://matcher.waves.exchange')
    pw.setNode('https://nodes.wavesnodes.com')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "buy", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentDiscountedBuyingFee(priceAssetId, price, amount)

    assert calculatedFee >= requestedFees['discount']['matcherFee']

def test_getCalculatePercentDiscountedSellingFee():
    pw.setMatcher('https://matcher.waves.exchange')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "sell", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentDiscountedSellingFee(priceAssetId, amountAssetId, amount)

    assert calculatedFee >= requestedFees['discount']['matcherFee']

def test_getCalculatePercentBuyingFee_01():
    pw.setMatcher('https://matcher.waves.exchange')
    pw.setNode('https://nodes.wavesnodes.com')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = '34N9YcEETLWn93qYQ64EsP1x89tSruJU44RrEMSXXEPJ'
    amountAssetId = 'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on'
    price = 109185
    amount = 999000000
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "buy", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)

    assert calculatedFee >= requestedFees['base']['matcherFee']

def test_getCalculatePercentBuyingFee_02():
    pw.setMatcher('https://matcher.waves.exchange')
    pw.setNode('https://nodes.wavesnodes.com')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 1 * 10 ** 6
    amount = 1 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "buy", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)

    assert calculatedFee >= requestedFees['base']['matcherFee']

def test_getCalculatePercentBuyingFee_03():
    pw.setMatcher('https://matcher.waves.exchange')
    pw.setNode('https://nodes.wavesnodes.com')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 100 * 10 ** 6
    amount = 100 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "buy", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentBuyingFee(amountAssetId, priceAssetId, price, amount)

    assert calculatedFee >= requestedFees['base']['matcherFee']

def test_getCalculatePercentSellingFee():
    pw.setMatcher('https://matcher.waves.exchange')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'WAVES'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "sell", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculatePercentSellingFee(priceAssetId, amountAssetId, amount)

    assert calculatedFee >= requestedFees['base']['matcherFee']

def test_discountedFee():
    pw.setMatcher('https://matcher.waves.exchange')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'bPWkA3MNyEr1TuDchWgdpqJZhGhfPXj7dJdr3qiW2kD'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "sell", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculateDynamicDiscountFee()

    assert calculatedFee >= requestedFees['discount']['matcherFee']

def test_dynamicFee():
    pw.setMatcher('https://matcher.waves.exchange')
    matcher = 'https://matcher.waves.exchange'
    priceAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'
    amountAssetId = 'bPWkA3MNyEr1TuDchWgdpqJZhGhfPXj7dJdr3qiW2kD'
    price = 10 * 10 ** 6
    amount = 10 * 10 ** 8
    wxFeeCalculator = WXFeeCalculator()

    requestedFees = requests.post(
        matcher + '/matcher/orderbook/' + amountAssetId + '/' + priceAssetId + '/calculateFee',
        json={"orderType": "sell", "amount": amount, "price": price}).json()

    calculatedFee = wxFeeCalculator.calculateDynamicFee()

    assert calculatedFee >= requestedFees['base']['matcherFee']
