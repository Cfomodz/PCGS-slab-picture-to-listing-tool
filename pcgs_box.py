from datetime import datetime
import uuid
import json
import winsound
from coin import Coin
import keyboard
import time

from pcgs_api import PCGSApi


class Box:
    def __init__(self, barcode=None):
        self.coins = []
        self.total_value = 0
        self.barcode = barcode or str(uuid.uuid4())

    def add_coin(self, coin):
        if len(self.coins) < 20:
            if self.is_duplicate(coin):
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                print(f"Warning: Duplicate coin detected - {coin.year} {coin.denomination}")
                return False
            self.coins.append(coin)
            self.total_value += coin.price_guide_value
            return True
        else:
            print("Box is full. Cannot add more coins.")
            return False

    def is_duplicate(self, new_coin):
        return any(coin.year == new_coin.year and coin.denomination == new_coin.denomination and 
                coin.grade == new_coin.grade and coin.metal_content == new_coin.metal_content for coin in self.coins)

    def is_full(self):
        return len(self.coins) >= 20

    def process_barcode(self, barcode_str, last_processed_barcode, headers):
        if len(barcode_str) >= 16:
            if barcode_str != last_processed_barcode:
                grading_service = "PCGS" if len(barcode_str) == 16 else "NGC"
                coin = PCGSApi.make_api_call(barcode_str, grading_service)
                if self.add_coin(coin):
                    print(f"Added coin to box. Current count: {len(self.coins)}")
                    self.create_box_report()
                    return barcode_str
                elif self.is_duplicate(coin):
                    print("Duplicate coin detected. Not adding to box.")
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                elif self.is_full():
                    print("Box is full. Cannot add more coins.")
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    self.print_label()
                else:
                    print("Error adding coin to box.")
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
            else:
                print("Same barcode detected. Skipping API call.")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        else:
            print(f"Invalid barcode length: {len(barcode_str)}. Expected 16 or more digits.")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        return last_processed_barcode

    def remove_last_coin(self):
        if self.coins:
            removed_coin = self.coins.pop()
            self.total_value -= removed_coin.price_guide_value
            return removed_coin
        else:
            print("No coins to remove.")
            return None

    def reset(self):
        self.coins.clear()
        self.total_value = 0

    def save_to_file(self):
        box_data = {
            "barcode": self.barcode,
            "total_value": self.total_value,
            "coins": [coin.__dict__ for coin in self.coins]
        }
        with open(f"{self.barcode}.json", "w") as file:
            json.dump(box_data, file)
        print(f"Box saved to {self.barcode}.json")

    @classmethod
    def load_from_file(cls, barcode):
        try:
            with open(f"{barcode}.json", "r") as file:
                box_data = json.load(file)
            box = cls(barcode=box_data["barcode"])
            box.total_value = box_data["total_value"]
            box.coins = [Coin(data) for data in box_data["coins"]]
            return box
        except FileNotFoundError:
            print(f"No box found with barcode {barcode}")
            return None

    def __str__(self):
        return f"Box with {len(self.coins)} coins, total value: ${self.total_value:.2f}, barcode: {self.barcode}"
    
def create_box_report_html(box):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Box Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    white-space: pre-wrap;
    overflow: hidden;
    height: 100vh;
    margin: 0;
    padding: 20px;
    box-sizing: border-box;
    background-color: #000;
    color: #fff; / Changed text color to white /
    display: flex;
    justify-content: center; / Centers content horizontally /
    align-items: center; / Centers content vertically /
    text-align: center; / Centers text within the content div /
}}
#content {{
    width: 100%;
    / The following positioning and animation are controlled via JavaScript /
    position: absolute;
    top: 100%;
}}
@keyframes scrollUp {{
    0% {{
        top: 100%;
    }}
    80% {{
        top: -10%;
    }}
    100% {{
        top: 100%;
    }}
}}
</style>
</head>
<body>
    <div id="content">
        {generate_box_report(box)}
    </div>
    <script src="box_report.js"></script>
</body>
</html>
"""
    html_path = "box_report.html"
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    print(f"Box report HTML file has been created: {html_path}")
    
def generate_box_report(box):
    report = f"Box PCGS Price Guide Value:\n${box.total_value:.2f}\n\nCoins in the box:\n"
    for i, coin in enumerate(box.coins, 1):
        grade_string = coin.grade.replace("PR", "PR ").replace("MS", "MS ").replace("DCAM", " DCAM")
        report += f"{i}. {coin.year} {grade_string} {coin.denomination}\n"
    report += f"\nLast Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return report

def create_box_report(box):
    report = f"Box PCGS Price Guide Value:\n"
    report += f"${box.total_value:.2f}\n\n"
    report += "Coins in the box:\n"
    # box.coins.sort(key=lambda coin: coin.price_guide_value, reverse=True)  # This is not compatible with removing (popping) coins.
    for i, coin in enumerate(box.coins, 1):
        grade_string = coin.grade.replace("PR", "PR ").replace("MS", "MS ").replace("DCAM", " DCAM")
        report += f"{coin.year} {grade_string} {coin.denomination} | ${coin.price_guide_value}\n"

    with open("output.txt", "w") as file:
        file.write(report)
    
    print("Box report saved as 'output.txt'")
    create_box_report_html(box)
    winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)

# def handle_box_mode(headers):
#     box = Box()
#     last_processed_barcode = None
#     barcode_data = []
#     last_digit_time = [time.time()]

#     on_key_event = create_on_key_event(barcode_data, last_digit_time)
#     keyboard.hook(on_key_event)

#     print("Box Mode: Scan up to 20 coins.")
#     print("Press Ctrl + Alt + F7 to remove the last added coin, or Ctrl + Alt + F8 to clear the box.")

#     while len(box.coins) < 20:
#         current_time = time.time()
#         if barcode_data and (current_time - last_digit_time[0]) > BARCODE_TIMEOUT:
#             barcode_str = ''.join(barcode_data)
#             print(f"Processing barcode: {barcode_str}")
#             last_processed_barcode = process_barcode(barcode_str, last_processed_barcode, box, headers)
#             barcode_data.clear()

#         elif keyboard.is_pressed('ctrl+alt+f7'):
#             removed_coin = box.remove_last_coin()
#             if removed_coin:
#                 print(f"Removed last coin: {removed_coin.year} {removed_coin.denomination}")
#                 create_box_report(box)
#             else:
#                 print("No coins to remove.")
#             time.sleep(0.2)  # Reduced delay
#         elif keyboard.is_pressed('ctrl+alt+f8'):
#             box.reset()
#             print("Box cleared. All coins removed.")
#             create_box_report(box)
#             time.sleep(0.2)  # Reduced delay
#     print("Box is full. Cannot add more coins.")
#     keyboard.unhook(on_key_event)
#     create_box_report(box)
