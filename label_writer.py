import time
from PIL import Image
import barcode
from barcode.writer import ImageWriter
from coin import COIN_WEIGHTS
from barcode_scanner import BarcodeScanner
import os
import win32print
import win32api

def create_barcode(barcode_data):
    ean = barcode.get('code128', barcode_data, writer=ImageWriter())
    barcode_path = f"barcode_{barcode_data}"
    ean.save(barcode_path)
    
    return f"{barcode_path}.png"

def create_label(coin, toned_clad=False):
        # Create label content
        metal_content_content = coin.metal_content.split('over')[0] if coin.metal_content else ""
        metal_content_content = metal_content_content[0:26] if metal_content_content else ""
        label_content = f"{metal_content_content}\n"
        label_content += f"Pop Higher: {coin.pop_higher}\n"
        label_content += f"PCGS Price Guide: ${coin.price_guide_value}\n" if coin.price_guide_value else ""

        if coin.metal_content and "silver" in coin.metal_content.lower():
            silver_melt_price = 28.55  # Price per troy ounce
            coin_weight = COIN_WEIGHTS.get(coin.denomination, 0)  # Get weight based on denomination
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
    
def create_box_label_content(box):
    content = f"Box"
    content += f"Total Value: ${box.total_value:.2f}\n"
    content += "Coins:\n"
    for coin in box.coins:
        content += f"{coin.year} {coin.denomination} - ${coin.price_guide_value:.2f}\n"
    return content
    
def create_order_label(order):
    label_content = f"Order Target Value: ${order.target_value:.2f}\n"
    label_content += f"Remaining Value: ${order.remaining_value:.2f}\n"
    label_content += "Boxes:\n"
    for box in order.boxes:
        label_content += f"Box Barcode: {box.barcode} - Total Value: ${box.total_value:.2f}\n"
    return label_content

def create_order_label_content(order):
    content = f"Order Target Value: ${order.target_value:.2f}\n"
    content += f"Remaining Value: ${order.remaining_value:.2f}\n"
    content += "Boxes:\n"
    for box in order.boxes:
        content += f"Total Value: ${box.total_value:.2f}\n"
    return content

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

def create_label_document(item_name, sku, cost=None, auction_price=None, bin_price=None, barcode_data=None, label_number=1, date='Unknown Date'):
    # If no barcode data is supplied, use the SKU
    if not barcode_data:
        barcode_data = sku

    # Create document
    output_filename = f"tmp/label_{sku}.pdf"
    c = canvas.Canvas(output_filename, pagesize=(170, 70))

    # Header
    c.setFont("Helvetica-Bold", 14)  # Smaller font for item name
    c.drawString(10, 46, f"Slab # {label_number:03}")

    # Date
    c.setFont("Helvetica", 8)  # Smaller font for date
    c.drawString(10, 36, item_name)
    c.drawString(10, 26, date)

    # Auction Price & BIN Price
    c.setFont("Helvetica", 12)
    # if auction_price:
    #     c.drawString(10, 30, f"Auction Start: ${auction_price}")
    if bin_price:
        c.drawString(10, 12, f"BIN Price: ${bin_price}")

    # SKU
    c.setFont("Helvetica", 10) 
    c.drawString(10, 1, f"SKU: {sku}")

    c.save()

    print(f"Label saved as {output_filename}")
    return output_filename

def print_label_windows(pdf_file_path, printer_name):
    # Convert to absolute path
    absolute_path = os.path.abspath(pdf_file_path)
    
    # Check if file exists
    if not os.path.exists(absolute_path):
        print(f"File not found: {absolute_path}")
        return
    
    # Use ShellExecute to print the PDF using the default PDF viewer
    try:
        win32api.ShellExecute(
            0,
            "print",
            absolute_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
        print(f"Sent print job for {absolute_path} to printer {printer_name}")
    except Exception as e:
        print(f"Failed to print {absolute_path} to printer {printer_name}. Error: {e}")

if __name__ == "__main__":
    # Example usage
    pdf_file = create_label_document(
        item_name="PCGS PR69DCAM 1986-S $0.10",
        bin_price="35.00",
        sku="093554649577024",
        label_number=10,
        date="Thursday, September 26, 2024"
    )

    print_label_windows(pdf_file, "Brother QL-710W")

