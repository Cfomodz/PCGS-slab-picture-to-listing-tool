from core.label_writer import LabelWriter
from reportlab.pdfgen import canvas
from typing import Any, Optional
from plugins.coin.coin import COIN_WEIGHTS

class CoinLabelWriter(LabelWriter):
    def create_label_content(self, coin: Any, toned_clad: bool = False) -> str:
        metal_content_content = coin.metal_content.split('over')[0] if coin.metal_content else ""
        metal_content_content = metal_content_content[0:26] if metal_content_content else ""
        label_content = f"{metal_content_content}\n"
        label_content += f"Pop Higher: {coin.pop_higher}\n"
        label_content += f"PCGS Price Guide: ${coin.price_guide_value}\n" if coin.price_guide_value else ""

        if coin.metal_content and "silver" in coin.metal_content.lower():
            silver_melt_price = 28.55  # Price per troy ounce
            coin_weight = COIN_WEIGHTS.get(coin.denomination, 0)
            try:
                silver_fineness = float(coin.metal_content.split('%')[0]) / 100 if '%' in coin.metal_content else 1
            except:
                silver_fineness = 0.4
            silver_melt_value = round(silver_melt_price * coin_weight * silver_fineness, 2)
            if toned_clad:
                tuesdays_price = coin.price_guide_value
            else:
                tuesdays_price = round((coin.price_guide_value - silver_melt_value) / 2 + silver_melt_value, 2) if coin.price_guide_value else 0
            label_content += f"Silver Melt Value: ${silver_melt_value}\n"
            label_content += f"Starting Bid: ${tuesdays_price}\n"
        else:
            half_price = round(coin.price_guide_value / 2, 2) if coin.price_guide_value else 0
            label_content += f"Starting Bid: ${half_price}\n"
        return label_content

    def create_label_document(self, coin: Any, sku: Optional[str] = None, label_number: int = 1, date: str = 'Unknown Date', bin_price: Optional[float] = None) -> str:
        if not sku:
            sku = getattr(coin, 'cert_no', getattr(coin, 'sku', 'unknown'))
        output_filename = f"tmp/label_{sku}.pdf"
        c = canvas.Canvas(output_filename, pagesize=(170, 70))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(10, 46, f"Slab # {label_number:03}")
        c.setFont("Helvetica", 8)
        c.drawString(10, 36, getattr(coin, 'name', ''))
        c.drawString(10, 26, date)
        c.setFont("Helvetica", 12)
        if bin_price:
            c.drawString(10, 12, f"BIN Price: ${bin_price}")
        c.setFont("Helvetica", 10)
        c.drawString(10, 1, f"SKU: {sku}")
        c.save()
        print(f"Label saved as {output_filename}")
        return output_filename 