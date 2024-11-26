import time
import keyboard
import cv2
from PIL import Image
from pyzbar.pyzbar import decode
from pcgs_api import PCGSApi
from pcgs_box import Box
import threading
import winsound

class CameraMonitor:
    def __init__(self):
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            cap = cv2.VideoCapture(1)  # Adjust the camera index if needed
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    with self.lock:
                        self.frame = frame
                cap.release()
            time.sleep(0.1)  # Adjust the delay as needed

    def read(self):
        with self.lock:
            return self.frame

    def stop(self):
        self.stopped = True

class BarcodeScanner:
    MAX_BARCODE_LENGTH = 20
    BARCODE_TIMEOUT = 1.12

    def __init__(self):
        self.api = PCGSApi()
        self.last_processed_barcode = None
        self.barcode_data = []
        self.last_digit_time = [time.time()]

    def create_on_key_event(self):
        def on_key_event(event):
            current_time = time.time()
            if event.event_type == 'down' and event.name.isdigit():
                self.barcode_data.append(event.name)
                self.last_digit_time[0] = current_time
        return on_key_event

    def get_frame_from_camera(self):
        cap = cv2.VideoCapture(1)  # Use 0 for default camera, adjust if needed
        ret, frame = cap.read()
        cap.release()
        if ret:
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return None

    def scan_image_for_barcode(self, image_path):
        # Open the image using PIL
        image = Image.open(image_path)
        # Convert the image to grayscale
        grayscale_image = image.convert('L')
        # Decode the barcode from the grayscale image
        barcodes = decode(grayscale_image)
        if barcodes:
            return barcodes[0].data.decode('utf-8')
        return None

    def process_frame(self, image, return_coin=False):
        print("New frame captured")
        barcode = self.scan_image_for_barcode(image)
        if barcode:
            grading_service = "PCGS" if len(barcode) == 16 else "NGC"
            coin = self.api.make_api_call(barcode, grading_service)
            if return_coin:
                coin.barcode = barcode
                return coin
            label_content = self.create_label(coin)
            self.output_file(label_content)
            return True
        return False

    def monitor_camera(self):
        print("Monitoring camera for barcodes. Press 'q' to quit.")
        camera_monitor = CameraMonitor().start()
        self.last_processed_barcode = None

        while True:
            frame = camera_monitor.read()
            if frame is not None:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                barcode = self.scan_image_for_barcode(image)
                if barcode and barcode != self.last_processed_barcode:
                    if self.process_frame(image):
                        print("Barcode processed. Waiting for next barcode...")
                        self.last_processed_barcode = barcode
                elif barcode == self.last_processed_barcode:
                    print("Same barcode detected. Skipping API call.")
            
            if keyboard.is_pressed('q'):
                print("Quitting camera monitoring.")
                break
            
            time.sleep(1.5)  # Check every half second

        camera_monitor.stop()

    def monitor_scanner(self, headers):
        self.barcode_data = []
        self.last_digit_time = [time.time()]

        on_key_event = self.create_on_key_event()
        keyboard.hook(on_key_event)

        self.last_processed_barcode = None

        print("Waiting for barcode scan... Press 'q' to quit.")

        while True:
            time.sleep(1.5)
            current_time = time.time()
            if self.barcode_data and (current_time - self.last_digit_time[0]) > self.BARCODE_TIMEOUT:
                barcode_str = ''.join(self.barcode_data)
                if len(barcode_str) >= 16:
                    print(f"Barcode data received: {barcode_str}")
                    if barcode_str != self.last_processed_barcode:
                        grading_service = "PCGS" if len(barcode_str) == 16 else "NGC"
                        coin = self.api.make_api_call(barcode_str, grading_service)
                        label_content = self.create_label(coin)
                        self.output_file(label_content)
                        self.last_processed_barcode = barcode_str
                        print("Waiting for barcode scan...")
                    else:
                        print("Same barcode detected. Skipping API call.")
                    self.barcode_data.clear()
                else:
                    print(f"Invalid barcode length: {len(barcode_str)}. Expected 16 or more digits.")
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    self.barcode_data.clear()
            
            if keyboard.is_pressed('q'):
                print("Quitting scanner monitoring.")
                break

        keyboard.unhook(on_key_event)

    