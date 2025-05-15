from typing import Any, Dict, List
from core.base import ItemScanner
from core.plugin import PluginRegistry
from core.barcode_scanner import BarcodeScanner
from plugins.coin.pcgs_api import PCGSApi

class CoinScanner(ItemScanner):
    """
    Scans images of coins and extracts relevant data using BarcodeScanner and PCGSApi.
    """
    def __init__(self):
        self.barcode_scanner = BarcodeScanner()
        self.api = PCGSApi()

    def scan(self, images: List[Any]) -> Dict[str, Any]:
        # Try each image until a cert number is found and coin data is fetched
        for image in images:
            cert_number = self.barcode_scanner.scan_image_for_barcode(image)
            if cert_number:
                grading_service = "PCGS" if len(cert_number) == 16 else "NGC"
                coin = self.api.make_api_call(cert_number, grading_service)
                if coin:
                    return coin.to_dict() if hasattr(coin, 'to_dict') else dict(coin)
        return {'error': 'No coin identified from images.'}

# Register the scanner
PluginRegistry.register_scanner('coin', CoinScanner) 