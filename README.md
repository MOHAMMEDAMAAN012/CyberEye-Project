# Initialize local repo
git init CyberEye
cd CyberEye
# Create your files


🧩 Folder & File Structure
CyberEye/
│
├── core_engine.py
├── cybereye_ui.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

🧾 .gitignore (Python)
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.env/
.venv/

# IDE files
.vscode/
.idea/

# macOS
.DS_Store

# 🛡️ CyberEye – Desktop Antivirus Scanner with Real-Time Threat Detection

CyberEye is a modern, desktop-based antivirus scanner built using **Python** and **PySide6 (Qt)**.  
It uses **multi-threaded scanning** and **MD5 signature-based detection** to identify potential malware in any folder on your computer.

---

## 🧠 Features

✅ Recursive folder scanning  
✅ Multi-threaded processing (10 workers)  
✅ Real-time progress updates via Qt signals  
✅ Modern desktop GUI built with PySide6  
✅ Signature-based malware detection  
✅ Cross-platform support (Windows, macOS, Linux)

---

## 🧩 Architecture Overview

CyberEye is built using a **two-tier architecture**:

### 1. Frontend (GUI)
- Built with PySide6  
- Handles folder selection, progress updates, and displaying results  
- Uses signals and slots for thread-safe updates

### 2. Backend (Core Engine)
- Implements multi-threaded scanning  
- Uses MD5 hash-based signature matching  
- Efficient chunk-based file reading

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/CyberEye.git
cd CyberEye
python -m venv .venv
.venv\Scripts\activate      # or source .venv/bin/activate (Mac/Linux)
pip install -r requirements.txt

## RUN
python cybereye_ui.py

📂 File Structure
CyberEye/
├── core_engine.py        # Scanning logic (threaded)
├── cybereye_ui.py        # GUI interface (PySide6)
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── LICENSE               # Open-source license
└── .gitignore

🧮 Technical Details

Feature	Description
Hash Algorithm	MD5
Threads	10 concurrent
GUI Toolkit	PySide6 (Qt 6)
Language	Python 3.x
Detection Type	Signature-based
Target OS	Windows / macOS / Linux


🧰 Future Enhancements

Scan cancellation (Stop button)
Quarantine system
Heuristic detection
Real-time background protection
Custom signature database
Exportable scan reports

🧑‍💻 Author 
[Mohammed Amaan]
📅 November 2025
