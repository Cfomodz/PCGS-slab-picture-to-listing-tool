COIN_WEIGHTS = {
    "10C": 0.0800,   # Dime
    "25C": 0.2000,   # Quarter
    "50C": 0.4000,   # Half Dollar
    "$1": 0.8594,    # Silver Dollar
}

class Coin:
    def __init__(self, data):
        self.pcgs_no = data.get("PCGSNo", "")
        self.cert_no = data.get("CertNo", "")
        self.barcode = data.get("Barcode", "")
        self.name = data.get("Name", "")
        self.year = data.get("Year", 0)
        self.denomination = data.get("Denomination", "")
        self.mintage = data.get("Mintage", "")
        self.mint_mark = data.get("MintMark", "")
        self.mint_location = data.get("MintLocation", "")
        self.metal_content = data.get("MetalContent", "")
        self.diameter = data.get("Diameter", 0)
        self.edge = data.get("Edge", "")
        self.weight = data.get("Weight", 0)
        self.country = data.get("Country", "")
        self.grade = data.get("Grade", "")
        self.designation = data.get("Designation", "")
        self.price_guide_value = data.get("PriceGuideValue", 0)
        self.population = data.get("Population", 0)
        self.pop_higher = data.get("PopHigher", 0)
        self.coin_facts_link = data.get("CoinFactsLink", "")
        self.designer = data.get("Designer", "")
        self.images = data.get("Images", [])
        self.coin_facts_notes = data.get("CoinFactsNotes", "")
        self.major_variety = data.get("MajorVariety", "")
        self.minor_variety = data.get("MinorVariety", "")
        self.die_variety = data.get("DieVariety", "")
        self.auction_list = data.get("AuctionList", [])
        self.series_name = data.get("SeriesName", "")
        self.category = data.get("Category", "")
        self.is_toned = data.get("IsToned", False)
        self.has_true_view_image = data.get("HasTrueViewImage", False)
        self.has_obverse_image = data.get("HasObverseImage", False)
        self.has_reverse_image = data.get("HasReverseImage", False)
        self.image_ready = data.get("ImageReady", False)
        self.is_nfc_secure = data.get("IsNFCSecure", False)
        self.is_valid_request = data.get("IsValidRequest", False)
        self.server_message = data.get("ServerMessage", "")
        
    def set_images(self, front_image_path, back_image_path):
        self.front_image_path = front_image_path
        self.back_image_path = back_image_path
    
    def __str__(self) -> str:
        return f"Coin(pcgs_no={self.pcgs_no}, cert_no={self.cert_no}, name={self.name}, year={self.year}, denomination={self.denomination}, mintage={self.mintage}, mint_mark={self.mint_mark}, mint_location={self.mint_location}, metal_content={self.metal_content}, diameter={self.diameter}, edge={self.edge}, weight={self.weight}, country={self.country}, grade={self.grade}, designation={self.designation}, price_guide_value={self.price_guide_value}, population={self.population}, pop_higher={self.pop_higher}, coin_facts_link={self.coin_facts_link}, designer={self.designer}, images={self.images}, coin_facts_notes={self.coin_facts_notes}, major_variety={self.major_variety}, minor_variety={self.minor_variety}, die_variety={self.die_variety}, auction_list={self.auction_list}, series_name={self.series_name}, category={self.category}, has_true_view_image={self.has_true_view_image}, has_obverse_image={self.has_obverse_image}, has_reverse_image={self.has_reverse_image}, image_ready={self.image_ready}, is_nfc_secure={self.is_nfc_secure}, is_valid_request={self.is_valid_request}, server_message={self.server_message})"
    
    def to_dict(self):
        return self.__dict__
    
    
