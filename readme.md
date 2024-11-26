# PCGS Slab Picture to Listing Tool

A Python-based system for managing PCGS graded coin listing, scanning, labeling, and order management using the PCGS API. This project facilitates the efficient handling of incoming and outgoing coin orders: scanning barcodes, retrieving coin details, generating labels, managing orders, and generating detailed reports. Note. A lot of this was built to be integrated into OBS via dynamic text sources, local file browser source(s), etc. Though that is not in any way required, it is an easy way to put most of the outputs to use.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Scanning Barcodes](#scanning-barcodes)
  - [Managing Orders](#managing-orders)
  - [Generating Labels and Reports](#generating-labels-and-reports)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Barcode Scanning:** Utilize handheld or wireless scanners to input coin barcodes.
- **API Integration:** Fetch detailed coin information from the PCGS API.
- **Caching Mechanism:** Reduce unnecessary API calls by caching previously scanned data.
- **Label Generation:** Create and print labels for individual coins, boxes, and orders.
- **Order Management:** Organize coins into boxes and manage orders based on target values.
- **Reporting:** Generate HTML and text-based reports for boxes and orders.
- **User-Friendly Interface:** Although primarily command-line based, the system is designed to be extended with GUI capabilities.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Cfomodz/PCGS-slab-picture-to-listing-tool.git
   cd PCGS-slab-picture-to-listing-tool
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **API Key Setup**

   Obtain your PCGS API key and set it as an environment variable.

   ```bash
   export PCGS_API_KEY='your_api_key_here'  # On Windows: set PCGS_API_KEY=your_api_key_here
   ```

2. **Environment Variables**

   Create a `.env` file in the root directory to manage environment variables.

   ```env
   PCGS_API_KEY=your_api_key_here
   ```

## Usage

### Scanning Barcodes

You can scan coins using a barcode scanner or manually input barcodes. The system supports both real-time scanning via a connected camera and processing of saved barcode scans from a text file.

1. **Real-Time Scanning with Camera**

   ```bash
   python barcode_scanner.py
   ```

   - **Press `q`** to quit monitoring the camera.

2. **Processing Saved Scans**

   Place scanned barcodes in the `input_scans.txt` file and run:

   ```bash
   python pcgs_api.py
   ```

### Managing Orders

Create and manage orders based on target values. The system organizes coins into boxes and tracks the total value against the order's target.

1. **Start Order Management**

   ```bash
   python order_management.py
   ```

2. **Add or Remove Coins**

   - **Add Coins:** Scan barcodes to add coins to the current box.
   - **Remove Last Coin:** Press `Ctrl + Alt + F7`.
   - **Clear Box:** Press `Ctrl + Alt + F8`.
   - **Finalize Box:** Press `Ctrl + Alt + F9`.

### Generating Labels and Reports

Generate printable labels for coins, boxes, and orders, as well as detailed HTML reports.

1. **Generate Labels**

   ```bash
   python label_writer.py
   ```

2. **Generate Box Reports**

   ```bash
   python pcgs_box.py
   ```

3. **Generate Listing Labels**

   ```bash
   python listing.py
   ```

## Project Structure

PCGS-slab-picture-to-listing-tool/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pcgs_api.py
├── example_main.py
├── order_management.py
├── main.py
├── listing.py
├── pcgs_box.py
├── barcode_scanner.py
├── coin.py
├── label_writer.py
├── box_report.js
├── images/
├── tmp/
├── input_scans.txt
└── output.txt

### Description of Key Files

- **`pcgs_api.py`**: Handles API interactions with PCGS, including caching responses.
- **`barcode_scanner.py`**: Manages barcode scanning either via camera or scanner input.
- **`order_management.py`**: Facilitates the creation and management of orders, organizing coins into boxes.
- **`label_writer.py`**: Generates and prints labels for coins, boxes, and orders using ReportLab and system printers.
- **`pcgs_box.py`**: Manages individual boxes containing coins, including adding/removing coins and generating reports.
- **`listing.py`**: Handles the listing process, saving listings, and printing labels.
- **`main.py`**: Entry point for processing images and generating listings.
- **`box_report.js`**: JavaScript for dynamic box report animations.


## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the [GNU Lesser General Public License v2.1](LICENSE).

## Contact

For any questions or suggestions, please open an issue or create a PR.

---