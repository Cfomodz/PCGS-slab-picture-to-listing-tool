import pytest
from plugins.coin.coin_scanner import CoinScanner
from unittest.mock import patch, MagicMock

def test_coin_scanner_no_images():
    scanner = CoinScanner()
    result = scanner.scan([])
    assert 'error' in result
    assert result['error'] == 'No coin identified from images.'

def test_coin_scanner_identifies_coin():
    scanner = CoinScanner()
    dummy_coin = MagicMock()
    dummy_coin.to_dict.return_value = {'PCGSNo': '12345', 'Year': 2020}
    with patch.object(scanner.barcode_scanner, 'scan_image_for_barcode', side_effect=[None, '123456']):
        with patch.object(scanner.api, 'make_api_call', return_value=dummy_coin):
            images = ['img1.jpg', 'img2.jpg']
            result = scanner.scan(images)
            assert result == {'PCGSNo': '12345', 'Year': 2020} 