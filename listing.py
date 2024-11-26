from datetime import datetime
import json
from coin import Coin
from barcode_scanner import BarcodeScanner
from label_writer import print_label_windows, create_label_document

class Listing:
    def __init__(self, item=None, price_paid=None, listing_price=None, images=None, barcode_scanner=None):
        self.item = item
        self.price_paid = price_paid
        self.listing_price = listing_price
        self.images = images if images is not None else []
        self.BarcodeScanner = barcode_scanner

        if self.item is None and self.images:
            if self.BarcodeScanner is None:
                self.BarcodeScanner = BarcodeScanner()
            
            for image in self.images:
                coin = self.BarcodeScanner.process_frame(image, return_coin=True)
                if coin:
                    self.item = coin
                    break
    
    def to_dict(self):
        return {
            "item": self.item.__dict__,
            "price_paid": self.price_paid,
            "listing_price": self.listing_price,
            "images": self.images
        }
                
    def save_listing(self):
        with open("listings.json", "a") as f:
            json.dump(self.to_dict(), f)
            f.write("\n")
            
    def print_label(self, label_number):
        today = datetime.now().strftime("%Y-%m-%d")
        image_file = create_label_document(self.item.name, self.item.sku, cost=None, auction_price=None, bin_price=self.listing_price, barcode_data=None, label_number=label_number, date=today)
        print_label_windows(image_file, "Brother QL-710W")
