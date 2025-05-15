<div align="center">

# Coin Plugin for Object Scanning & Listing Tool (Core Backend)

**Barcode and image-based coin identification, listing, and label generation.**

</div>

---

## 🧩 What is this?

This repository is a **plugin** for the [Object Scanning & Listing Tool (Core Backend)](https://github.com/Cfomodz/Object-Scanning-Listing-Tool-Core-Backend-).  
It adds support for the "coin" item type, including:

- **CoinScanner**: Barcode/image-based coin identification
- **CoinListingBuilder**: Listing generation for coins
- **CoinLabelWriter**: Label creation for coins

> **Note:** This is **not a standalone tool**. It must be used with the core backend.

---

## 🚀 Quick Start

1. **Install the Core Backend**
   - See: [Core Backend README](https://github.com/Cfomodz/Object-Scanning-Listing-Tool-Core-Backend-)

2. **Install this Plugin**
   - Place this repo in the core backend's `plugins/coin/` directory:
     ```bash
     git clone https://github.com/Cfomodz/PCGS-slab-picture-to-listing-tool-plugin-coin plugins/coin
     ```
   - Install plugin dependencies:
     ```bash
     pip install -r plugins/coin/requirements.txt
     ```

3. **Configure**
   - Add your PCGS API key to `plugins/coin/.env`:
     ```env
     PCGS_API_KEY=your_key_here
     ```

4. **Run**
   - Use the core backend's CLI, specifying the `coin` item type:
     ```bash
     python main.py coin --images ./images
     ```

---

## 🧩 Plugin Architecture

- This plugin registers itself with the core system using the `PluginRegistry`.
- No manual registration is needed if placed in the correct directory.
- The core backend will auto-discover and use this plugin for all coin-related operations.

---

## 🛠️ Development & Testing

- Tests are in the `tests/` directory. Run with `pytest` from the plugin root.
- For development, ensure you have the core backend available and importable.

---

## 📜 License

LGPL-2.1

💌 Questions? Open an issue or join the Discord!
