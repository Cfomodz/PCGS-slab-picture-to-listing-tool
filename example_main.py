"""
This is more of an idea of how someone might want to use
the script, from a more user-friendly perspective (assuming
a GUI is implemented). Don't use this currently.
"""

# from barcode_scanner import BarcodeScanner
# from order_management import OrderManagement


# def main():
#     print("Choose initial mode: (C)amera, (S)canner, (B)ox, (O)rder, or (T)oned Clad?")
#     print("Defaulting to Scanner mode in 10 seconds...")
#     choice = input_with_timeout("Your choice: ", 10)

#     if choice is None:
#         print("No input received. Defaulting to Scanner mode.")
#         choice = 's'
#     elif choice not in ['c', 's', 'b', 'o', 't', 'i']:
#         print("Invalid choice. Defaulting to Scanner mode.")
#         choice = 's'

#     if choice == 'c':
#         monitor_camera()
#     elif choice == 'i':
#         look_up_saved_scans()
#     elif choice == 'o':
#         target_value = float(input("Enter the target PCGS price guide value for the order: "))
#         handle_order_mode(target_value)
#     elif choice == 't':
#         handle_toned_clad_mode()
#     else:
#         initial_mode = "scanner" if choice == 's' else "box"
#         run_mode(initial_mode)

# def main():
#     print("Choose initial mode: (S)canner or (O)rder?")
#     choice = input("Your choice: ").lower()

#     if choice == 's':
#         scanner = BarcodeScanner()
#         scanner.monitor_scanner()
#     elif choice == 'o':
#         target_value = float(input("Enter the target PCGS price guide value for the order: "))
#         order_manager = OrderManagement(target_value)
#         # TODO: order processing logic goes here
#     else:
#         print("Invalid choice.")

# if __name__ == "__main__":
#     main()

# import time
# def create_on_key_event(barcode_data, last_digit_time):
#     def on_key_event(event):
#         current_time = time.time()
#         if event.event_type == 'down' and event.name.isdigit():
#             barcode_data.append(event.name)
#             last_digit_time[0] = current_time
#     return on_key_event

# def input_with_timeout(prompt, timeout):
#     result = [None]
#     def get_input():
#         result[0] = input(prompt).lower()
#     thread = threading.Thread(target=get_input)
#     thread.daemon = True
#     thread.start()
#     thread.join(timeout)
#     return result[0]

# import keyboard
# import threading

# def toggle_mode(current_mode):
#     return "box" if current_mode == "scanner" else "scanner"

# def run_mode(mode, headers):
#     current_mode = mode
#     print(f"Starting in {current_mode.capitalize()} mode. Press Ctrl + Alt + F9 to switch modes.")
    
#     def mode_switch_listener():
#         nonlocal current_mode
#         while True:
#             if keyboard.is_pressed('ctrl+alt+f9'):
#                 current_mode = toggle_mode(current_mode)
#                 print(f"\nSwitching to {current_mode.capitalize()} mode.")
#                 time.sleep(0.5)

#     switch_thread = threading.Thread(target=mode_switch_listener, daemon=True)
#     switch_thread.start()

#     while True:
#         if current_mode == "scanner":
#             monitor_scanner(headers)
#         elif current_mode == "box":
#             handle_box_mode(headers)
#         else:
#             target_value = float(input("Enter the target PCGS price guide value for the order: "))
#             handle_order_mode(headers, target_value)
        
#         print(f"\nRestarting {current_mode.capitalize()} mode. Press Ctrl + Alt + F9 to switch modes.")
#         time.sleep(1)