COIN_WEIGHTS = {
    "10C": 0.0800,   # Dime
    "25C": 0.2000,   # Quarter
    "50C": 0.4000,   # Half Dollar
    "$1": 0.8594,    # Silver Dollar
}

from typing import Any, Dict, Optional

class Coin:
    """Represents a coin with all relevant attributes."""
    def __init__(self, data: Dict[str, Any]):
        self.pcgs_no: str = data.get("PCGSNo", "")
        self.cert_no: str = data.get("CertNo", "")
        self.barcode: str = data.get("Barcode", "")
        self.name: str = data.get("Name", "")
        self.year: int = data.get("Year", 0)
        self.denomination: str = data.get("Denomination", "")
        self.mintage: str = data.get("Mintage", "")
        self.mint_mark: str = data.get("MintMark", "")
        self.mint_location: str = data.get("MintLocation", "")
        self.metal_content: str = data.get("MetalContent", "")
        self.diameter: float = data.get("Diameter", 0)
        self.edge: str = data.get("Edge", "")
        self.weight: float = data.get("Weight", 0)
        self.country: str = data.get("Country", "")
        self.grade: str = data.get("Grade", "")
        self.designation: str = data.get("Designation", "")
        self.price_guide_value: float = data.get("PriceGuideValue", 0)
        self.population: int = data.get("Population", 0)
        self.pop_higher: int = data.get("PopHigher", 0)
        self.coin_facts_link: str = data.get("CoinFactsLink", "")
        self.designer: str = data.get("Designer", "")
        self.images: list = data.get("Images", [])
        self.coin_facts_notes: str = data.get("CoinFactsNotes", "")
        self.major_variety: str = data.get("MajorVariety", "")
        self.minor_variety: str = data.get("MinorVariety", "")
        self.die_variety: str = data.get("DieVariety", "")
        self.auction_list: list = data.get("AuctionList", [])
        self.series_name: str = data.get("SeriesName", "")
        self.category: str = data.get("Category", "")
        self.is_toned: bool = data.get("IsToned", False)
        self.has_true_view_image: bool = data.get("HasTrueViewImage", False)
        self.has_obverse_image: bool = data.get("HasObverseImage", False)
        self.has_reverse_image: bool = data.get("HasReverseImage", False)
        self.image_ready: bool = data.get("ImageReady", False)
        self.is_nfc_secure: bool = data.get("IsNFCSecure", False)
        self.is_valid_request: bool = data.get("IsValidRequest", False)
        self.server_message: str = data.get("ServerMessage", "")

    def set_images(self, front_image_path: str, back_image_path: str) -> None:
        """Set the file paths for the coin's images."""
        self.front_image_path = front_image_path
        self.back_image_path = back_image_path
    
    def __str__(self) -> str:
        return f"Coin(pcgs_no={self.pcgs_no}, cert_no={self.cert_no}, name={self.name}, year={self.year}, denomination={self.denomination}, mintage={self.mintage}, mint_mark={self.mint_mark}, mint_location={self.mint_location}, metal_content={self.metal_content}, diameter={self.diameter}, edge={self.edge}, weight={self.weight}, country={self.country}, grade={self.grade}, designation={self.designation}, price_guide_value={self.price_guide_value}, population={self.population}, pop_higher={self.pop_higher}, coin_facts_link={self.coin_facts_link}, designer={self.designer}, images={self.images}, coin_facts_notes={self.coin_facts_notes}, major_variety={self.major_variety}, minor_variety={self.minor_variety}, die_variety={self.die_variety}, auction_list={self.auction_list}, series_name={self.series_name}, category={self.category}, has_true_view_image={self.has_true_view_image}, has_obverse_image={self.has_obverse_image}, has_reverse_image={self.has_reverse_image}, image_ready={self.image_ready}, is_nfc_secure={self.is_nfc_secure}, is_valid_request={self.is_valid_request}, server_message={self.server_message})"
    
    def to_dict(self) -> dict:
        """Return a dictionary representation of the coin."""
        return self.__dict__ 