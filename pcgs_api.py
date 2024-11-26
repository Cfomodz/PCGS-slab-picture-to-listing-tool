import os
import requests
import json
import time
from dotenv import load_dotenv
from coin import Coin

# Load environment variables from .env file
load_dotenv()

class PCGSApi:
    def __init__(self):
        self.api_key = os.getenv('PCGS_API_KEY')
        # print(self.api_key)
        self.endpoint = "https://api.pcgs.com/publicapi/coindetail/GetCoinFactsByBarcode"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.cache_file = "coin_cache.json"

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self, cache):
        """
        So we don't have to make as many API calls when scanning a coin more than once.
        """
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f)

    def make_api_call(self, barcode, grading_service):
        cache = self.load_cache()
        print(barcode)
        
        if barcode in cache:
            print(f"Using cached data for barcode: {barcode}")
            coin = Coin(cache[barcode])
        else:
            time.sleep(1.5)  # Delay between processing api calls
            params = {
                "barcode": barcode,
                "gradingService": grading_service
            }
            
            print(f"Making request to {self.endpoint} with params: {params}")

            # Make the API request
            print(self.headers)
            print(params)
            response = requests.get(self.endpoint, headers=self.headers, params=params)

            # Check the response status code
            if response.status_code == 200:
                try:
                    data = response.json()
                    cache[barcode] = data  # Store the response in the cache
                    self.save_cache(cache)  # Save the updated cache to file
                except:
                    print(response.text)
                    return None
                
                coin = Coin(data)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        return coin
    
    def get_price_guide_value(self, barcode, grading_service, return_coin=False):
        coin = self.make_api_call(barcode, grading_service)
        if return_coin:
            return coin
        else:
            return float(coin.price_guide_value) if coin and coin.price_guide_value else 0.0

import winsound
def output_file(content):
    with open("output.txt", "w") as file:
        file.write(content)
    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
    
from label_writer import create_label
def look_up_saved_scans():
    """
    # When scanning in with a handheld/wireless scanner
    # It is much faster to just scan them one after another,
    # to a text document, and then look up the saved scans later.
    """
    api = PCGSApi()
    with open("input_scans.txt", "r") as file:
        for line in file:
            barcode_str = line.strip()  # Remove whitespace/newlines
            
            if len(barcode_str) >= 16:
                print(f"Processing barcode: {barcode_str}")
                
                if barcode_str != last_processed_barcode:
                    # Determine grading service based on barcode length
                    if len(barcode_str) == 16:
                        grading_service = "PCGS"
                    elif len(barcode_str) == 20:
                        grading_service = "NGC"
                    else: # This is needed because there are some SP coins != 16 that *are* PCGS
                        grading_service = "PCGS"
                        
                    # Process the coin
                    coin = api.make_api_call(barcode_str, grading_service)
                    if coin:
                        label_content = create_label(coin)
                        output_file(label_content)
                        last_processed_barcode = barcode_str
                        print("Ready for next barcode...")
                else:
                    print("Duplicate barcode detected. Skipping...")
            else:
                print(f"Invalid barcode length: {len(barcode_str)}. Expected 16 or more digits.")
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                
    print("Finished processing all saved scans.")