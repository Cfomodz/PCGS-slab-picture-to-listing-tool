<div align="center">

# PCGS Slab Tool  
![GitHub License](https://img.shields.io/github/license/Cfomodz/PCGS-slab-picture-to-listing-tool)
![GitHub Sponsors](https://img.shields.io/github/sponsors/Cfomodz)
![Discord](https://img.shields.io/discord/425182625032962049)   
<img src="https://github.com/user-attachments/assets/26fa2e62-64ed-43de-b0df-4465947d512e" alt="Coin Scan Tool" width="400"/>   
### ✨ From barcode to listing in 3 commands ✨   
**Scan PCGS slabs → Generate listings & labels**  
</div>

## 🚀 Quick Start   

1. **Install**  
  ```bash
    git clone https://github.com/Cfomodz/PCGS-slab-picture-to-listing-tool.git
    cd PCGS-slab-picture-to-listing-tool && pip install -r requirements.txt
  ```

2. **Scan**
 ```bash
 python barcode_scanner.py  # Uses camera or scanner
 ```
   
3. **Print**
 ```
 python label_writer.py  # Auto-generates labels
 ```

## 🔑 Key Features   
    
  📦 1-Click Order Management (Ctrl+Alt shortcuts)   
  
  🖨️ Print labels for coins/boxes/orders   
  
  💾 Cached API calls to save requests   
  
  📊 Auto HTML reports for inventory   
  
  🎥 OBS-ready outputs via text/file sources

## ⚙️ Setup   

Add PCGS API key to .env:

```python
  PCGS_API_KEY=your_key_here
```

## 🛠️ Need Help?    

### Scanning Issues?    

Use your barcode scanner to scan the slabs into a text file then   

```bash
  python pcgs_api.py --file input_scans.txt
```

### Wrong Entry?   

Ctrl+Alt+F7 = undo last scan

---

📜 License: LGPL-2.1   
💌 Questions? Open an issue

</div>
