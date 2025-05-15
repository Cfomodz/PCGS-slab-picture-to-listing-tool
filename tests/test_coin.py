import pytest
from plugins.coin.coin import Coin

def test_coin_instantiation():
    data = {
        "PCGSNo": "12345",
        "CertNo": "67890",
        "Barcode": "1111222233334444",
        "Name": "Test Coin",
        "Year": 2020,
        "Denomination": "25C",
        "PriceGuideValue": 100.0
    }
    coin = Coin(data)
    assert coin.pcgs_no == "12345"
    assert coin.cert_no == "67890"
    assert coin.barcode == "1111222233334444"
    assert coin.name == "Test Coin"
    assert coin.year == 2020
    assert coin.denomination == "25C"
    assert coin.price_guide_value == 100.0 