import os
import requests
import time
from plugins.coin.coin import Coin
from core.barcode_scanner import BarcodeScanner
from dotenv import load_dotenv

# Load plugin-specific .env if present
plugin_env = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(plugin_env):
    load_dotenv(dotenv_path=plugin_env, override=True)

class PCGSApi:
    def __init__(self):
        self.api_key = os.getenv('PCGS_API_KEY')
        if not self.api_key:
            print("[ERROR] PCGS_API_KEY is missing. Please set it in your .env file or environment variables.")
        self.endpoint = "https://api.pcgs.com/publicapi/coindetail/GetCoinFactsByBarcode"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
        self.cache_file = "coin_cache.json"

    def load_cache(self):
        if os.path.exists(os.path.join('logs', self.cache_file)):
            return BarcodeScanner.load_json(self.cache_file)
        return {}

    def save_cache(self, cache):
        BarcodeScanner.save_json(self.cache_file, cache)

    def make_api_call(self, cert_number, grading_service):
        if not self.api_key:
            print("[ERROR] Cannot make API call: PCGS_API_KEY is missing.")
            return None
        cache = self.load_cache()
        if cert_number in cache:
            print(f"Using cached data for cert number: {cert_number}")
            coin = Coin(cache[cert_number])
        else:
            time.sleep(1.5)
            params = {
                "barcode": cert_number,
                "gradingService": grading_service
            }
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            if response.status_code == 200:
                try:
                    data = response.json()
                    cache[cert_number] = data
                    self.save_cache(cache)
                except Exception:
                    print(response.text)
                    return None
                coin = Coin(data)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        return coin

    def get_price_guide_value(self, cert_number, grading_service, return_coin=False):
        coin = self.make_api_call(cert_number, grading_service)
        if return_coin:
            return coin
        else:
            return float(coin.price_guide_value) if coin and coin.price_guide_value else 0.0 