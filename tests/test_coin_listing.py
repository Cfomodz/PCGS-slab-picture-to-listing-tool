import pytest
from plugins.coin.coin_listing import CoinListingBuilder

def test_coin_listing_builder_keep():
    builder = CoinListingBuilder()
    item_data = {
        'Year': 2020,
        'Denomination': '25C',
        'MintMark': 'P',
        'Name': 'Test Coin',
        'Grade': 'MS70',
        'CertNo': '123456',
        'Images': ['img1.jpg'],
        'Category': 'Coins',
        'PriceGuideValue': 100.0
    }
    listing = builder.build_listing(item_data)
    assert listing['verdict'] == 'keep'
    assert listing['title'].startswith('2020 25C')
    assert listing['attributes']['PriceGuideValue'] == 100.0

def test_coin_listing_builder_toss():
    builder = CoinListingBuilder()
    item_data = {
        'Year': 2020,
        'Denomination': '25C',
        'MintMark': 'P',
        'Name': 'Test Coin',
        'Grade': 'MS70',
        'CertNo': '123456',
        'Images': ['img1.jpg'],
        'Category': 'Coins',
        'PriceGuideValue': 0.0
    }
    listing = builder.build_listing(item_data)
    assert listing['verdict'] == 'toss' 