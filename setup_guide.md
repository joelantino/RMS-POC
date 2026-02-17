# AI Activity Tracker: Setup Guide (Mac & Windows)

This guide provides step-by-step instructions to get the **AI Activity Tracker** running as a background application on both macOS and Windows.

---

## 🏗️ 1. Prerequisites (For Both Platforms)

### **A. Install Python**
Ensure you have Python 3.8+ installed. 
- **Windows**: Download from [python.org](https://www.python.org/downloads/windows/).
- **Mac**: `brew install python` (requires Homebrew).

### **B. Install Ollama (The AI Engine)**
The tracker uses Ollama to handle all AI processing locally for privacy.
1. Download Ollama from [ollama.com](https://ollama.com/).
2. Run the following command in your terminal to download the Llama 3.2 model:
   ```bash
   ollama run llama3.2
   ```

### **C. Install Tesseract OCR**
Tesseract is needed to read text from your screen.
- **Windows**: 
  1. Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
  2. Install it (default path is usually `C:\Program Files\Tesseract-OCR`).
- **Mac**:
  1. Install via Homebrew:
     ```bash
     brew install tesseract
     ```

---

## 🐍 2. Python Environment Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/joelantino/RMS-POC.git
   cd RMS-POC
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *If you don't have a requirements.txt, run:*
   ```bash
   pip install mss pytesseract pillow requests pystray
   ```

---

## 🚀 3. Running the Application

### **Option A: Run as Script (Recommended for testing)**
Run the tray application directly:
```bash
python tray_app.py
```
- You will see a blue icon in your **System Tray** (Windows) or **Menu Bar** (Mac).
- **Right-click** the icon to Start/Stop tracking.

### **Option B: Create a Standalone Executable**
If you want a double-clickable `.exe` or `.app` file:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the app:
   - **Windows**: `pyinstaller --noconsole --onefile --name "AIActivityTracker" tray_app.py`
   - **Mac**: `pyinstaller --noconsole --onefile --name "AIActivityTracker" --windowed tray_app.py`

---

## 🧹 4. Automatic Cleanup
The app is designed to be **Zero-Footprint**:
- Screenshots are deleted immediately after reading.
- Raw logs are wiped after the final report is generated.
- Old reports are cleared on the start of a new day.

---

## 🛠️ Troubleshooting
- **macOS Permissions**: On Mac, you must allow your terminal (or the packaged app) **"Screen Recording"** permissions in `System Settings > Privacy & Security`.
- **Ollama Error**: Ensure the Ollama app is running in the background.
- **OCR Error**: Ensure Tesseract is installed and available in your system's PATH.
