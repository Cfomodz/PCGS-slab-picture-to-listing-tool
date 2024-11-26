from pcgs_api import PCGSApi
from pcgs_box import Box
import json

class Order:
    def __init__(self, target_value):
        self.boxes = []
        self.target_value = target_value
        self.remaining_value = target_value

    def add_box(self, box):
        self.boxes.append(box)
        self.remaining_value -= box.total_value

    def is_duplicate(self, new_coin):
        for box in self.boxes:
            if box.is_duplicate(new_coin):
                return True
        return False

    def save_to_file(self):
        order_data = {
            "target_value": self.target_value,
            "remaining_value": self.remaining_value,
            "boxes": [box.barcode for box in self.boxes]
        }
        with open("order.json", "w") as file:
            json.dump(order_data, file)
        print("Order saved to order.json")

    @classmethod
    def load_from_file(cls):
        try:
            with open("order.json", "r") as file:
                order_data = json.load(file)
            order = cls(order_data["target_value"])
            order.remaining_value = order_data["remaining_value"]
            order.boxes = [Box.load_from_file(barcode) for barcode in order_data["boxes"]]
            return order
        except FileNotFoundError:
            print("No order found")
            return None

    def __str__(self):
        return f"Order with {len(self.boxes)} boxes, target value: ${self.target_value:.2f}, remaining value: ${self.remaining_value:.2f}"

    def process_order_barcode(self, barcode_str):
        if len(barcode_str) >= 16:
            grading_service = "PCGS" if len(barcode_str) == 16 else "NGC"
            coin = self.api.make_api_call(barcode_str, grading_service)
            if not self.order.is_duplicate(coin):
                if coin.price_guide_value <= self.remaining_value:
                    if self.current_box.add_coin(coin):
                        self.remaining_value -= coin.price_guide_value
                        print(f"Added coin to current box. Remaining value: ${self.remaining_value:.2f}")
                        return barcode_str
                    else:
                        print("Current box is full. Cannot add more coins.")
                else:
                    print(f"Coin value ${coin.price_guide_value:.2f} exceeds remaining target value ${self.remaining_value:.2f}. Skipping.")
            else:
                print("Duplicate coin detected in the order. Skipping.")
        else:
            print(f"Invalid barcode length: {len(barcode_str)}. Expected 16 or more digits.")
        return None
    

from pcgs_box import create_box_report
import winsound

def process_order_barcode(barcode_str, last_processed_barcode, current_box, order, headers, remaining_value):
    if len(barcode_str) >= 16:
        if barcode_str != last_processed_barcode:
            grading_service = "PCGS" if len(barcode_str) == 16 else "NGC"
            coin = PCGSApi.make_api_call(barcode_str, grading_service)
            if not order.is_duplicate(coin):
                if coin.price_guide_value <= remaining_value:
                    if current_box.add_coin(coin):
                        remaining_value -= coin.price_guide_value
                        print(f"Added coin to current box. Remaining value: ${remaining_value:.2f}")
                        create_box_report(current_box)
                        return barcode_str
                    else:
                        print("Current box is full. Cannot add more coins.")
                        winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                        winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
                else:
                    print(f"Coin value ${coin.price_guide_value:.2f} exceeds remaining target value ${remaining_value:.2f}. Skipping.")
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            else:
                print("Duplicate coin detected in the order. Skipping.")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        else:
            print("Same barcode detected. Skipping API call.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    else:
        print(f"Invalid barcode length: {len(barcode_str)}. Expected 16 or more digits.")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    return last_processed_barcode

def handle_order_modifications(order, headers):
    while True:
        action = input("Enter 'a' to add a coin, 'r' to remove a coin, or 'q' to quit: ").lower()
        if action == 'a':
            barcode_str = input("Enter the barcode of the coin to add: ")
            current_box = Box()
            # process_order_barcode(barcode_str, None, current_box, order, headers, order.remaining_value)
        elif action == 'r':
            box_index = int(input("Enter the box number to remove a coin from: ")) - 1
            if 0 <= box_index < len(order.boxes):
                removed_coin = order.boxes[box_index].remove_last_coin()
                if removed_coin:
                    order.remaining_value += removed_coin.price_guide_value
                    print(f"Removed coin: {removed_coin.year} {removed_coin.denomination}")
                    # create_box_report(order.boxes[box_index])
                else:
                    print("No coins to remove.")
            else:
                print("Invalid box number.")
        elif action == 'q':
            break
        else:
            print("Invalid action.")

def create_order_report(order):
    report = "Order Report:\n"
    for i, box in enumerate(order, 1):
        report += f"\nBox {i}:\n"
        # report += generate_box_report(box)
    with open("order_report.txt", "w") as file:
        file.write(report)
    print("Order report saved as 'order_report.txt'")
    # winsound.PlaySound("ba_dum_notification.wav", winsound.SND_FILENAME)
    
import keyboard
import time
from barcode_scanner import create_on_key_event, BARCODE_TIMEOUT
from label_writer import print_label

def handle_order_mode(headers, target_value):
    order = Order(target_value)
    last_processed_barcode = None
    barcode_data = []
    last_digit_time = [time.time()]
    current_box = None
    remaining_value = target_value

    on_key_event = create_on_key_event(barcode_data, last_digit_time)
    keyboard.hook(on_key_event)

    print(f"Order Mode: Target PCGS Price Guide Value: ${target_value:.2f}")
    print("Press Ctrl + Alt + F7 to remove the last added coin, or Ctrl + Alt + F8 to clear the current box.")
    print("Press Ctrl + Alt + F9 to finalize the current box and start a new one.")

    while remaining_value > 0:
        current_time = time.time()
        if barcode_data and (current_time - last_digit_time[0]) > BARCODE_TIMEOUT:
            barcode_str = ''.join(barcode_data)
            print(f"Processing barcode: {barcode_str}")
            if current_box is None:
                current_box = Box.load_from_file(barcode_str)
                if current_box is None:
                    current_box = Box()
                    print_label(f"Box Barcode:", barcode_str)
            last_processed_barcode = process_order_barcode(barcode_str, last_processed_barcode, current_box, order, headers, remaining_value)
            barcode_data.clear()

        elif keyboard.is_pressed('ctrl+alt+f7'):
            removed_coin = current_box.remove_last_coin()
            if removed_coin:
                remaining_value += removed_coin.price_guide_value
                print(f"Removed last coin: {removed_coin.year} {removed_coin.denomination}")
                create_box_report(current_box)
            else:
                print("No coins to remove.")
            time.sleep(0.2)
        elif keyboard.is_pressed('ctrl+alt+f8'):
            for coin in current_box.coins:
                remaining_value += coin.price_guide_value
            current_box.reset()
            print("Current box cleared. All coins removed.")
            create_box_report(current_box)
            time.sleep(0.2)
        elif keyboard.is_pressed('ctrl+alt+f9'):
            if current_box.coins:
                order.add_box(current_box)
                current_box.save_to_file()
                print_label(create_box_label_content(current_box), barcode_data=current_box.barcode)
                print(f"Box finalized. Total boxes in order: {len(order.boxes)}")
                current_box = Box()
                print_label(f"Box Barcode: {current_box.barcode}", barcode_data=current_box.barcode)
            else:
                print("Current box is empty. Cannot finalize an empty box.")
            time.sleep(0.2)  # Reduced delay
    keyboard.unhook(on_key_event)
    order.save_to_file()
    create_order_report(order)
    print(f"Order completed. Total value: ${target_value - remaining_value:.2f}")

    if input("Do you want to add/remove coins before finalizing the order? (y/n): ").lower() == 'y':
        handle_order_modifications(order, headers)

    create_order_label(order)
    print_label(create_order_label_content(order), )
    print("Order finalized.")
from label_writer import create_box_label_content, create_order_label, create_order_label_content