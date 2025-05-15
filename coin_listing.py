from typing import Any, Dict
from core.base import ListingBuilder
from core.plugin import PluginRegistry

class CoinListingBuilder(ListingBuilder):
    """
    Builds a listing dictionary for a coin from scanned data.
    """
    def build_listing(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        # Use all relevant fields from the Coin data model
        listing = {
            'title': f"{item_data.get('Year', '')} {item_data.get('Denomination', '')} {item_data.get('MintMark', '')}",
            'description': f"{item_data.get('Name', '')} Graded {item_data.get('Grade', '')}, Serial: {item_data.get('CertNo', '')}",
            'images': item_data.get('Images', []),
            'category': item_data.get('Category', 'Coins'),
            'attributes': {
                'PCGSNo': item_data.get('PCGSNo'),
                'CertNo': item_data.get('CertNo'),
                'Barcode': item_data.get('Barcode'),
                'Name': item_data.get('Name'),
                'Year': item_data.get('Year'),
                'Denomination': item_data.get('Denomination'),
                'Mintage': item_data.get('Mintage'),
                'MintMark': item_data.get('MintMark'),
                'MintLocation': item_data.get('MintLocation'),
                'MetalContent': item_data.get('MetalContent'),
                'Diameter': item_data.get('Diameter'),
                'Edge': item_data.get('Edge'),
                'Weight': item_data.get('Weight'),
                'Country': item_data.get('Country'),
                'Grade': item_data.get('Grade'),
                'Designation': item_data.get('Designation'),
                'PriceGuideValue': item_data.get('PriceGuideValue'),
                'Population': item_data.get('Population'),
                'PopHigher': item_data.get('PopHigher'),
                'CoinFactsLink': item_data.get('CoinFactsLink'),
                'Designer': item_data.get('Designer'),
                'CoinFactsNotes': item_data.get('CoinFactsNotes'),
                'MajorVariety': item_data.get('MajorVariety'),
                'MinorVariety': item_data.get('MinorVariety'),
                'DieVariety': item_data.get('DieVariety'),
                'AuctionList': item_data.get('AuctionList'),
                'SeriesName': item_data.get('SeriesName'),
                'IsToned': item_data.get('IsToned'),
                'HasTrueViewImage': item_data.get('HasTrueViewImage'),
                'HasObverseImage': item_data.get('HasObverseImage'),
                'HasReverseImage': item_data.get('HasReverseImage'),
                'ImageReady': item_data.get('ImageReady'),
                'IsNFCSecure': item_data.get('IsNFCSecure'),
                'IsValidRequest': item_data.get('IsValidRequest'),
                'ServerMessage': item_data.get('ServerMessage'),
            },
            'verdict': 'keep' if item_data.get('PriceGuideValue', 0) > 0 else 'toss',
        }
        return listing

# Register the builder
PluginRegistry.register_builder('coin', CoinListingBuilder) 