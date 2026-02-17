import shutil
import sys
import os
import requests
import subprocess

def check_python():
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_tesseract():
    # Check if tesseract is in PATH
    tess_path = shutil.which("tesseract")
    if tess_path:
        print(f"✅ Tesseract found at: {tess_path}")
        return True
    
    # Check common locations manually
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        fr"C:\Users\{os.getlogin()}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract found at: {path}")
            return True
            
    print("❌ Tesseract OCR NOT found!")
    print("   Please download and install it from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   (During installation, add Tesseract to PATH for easier usage)")
    return False

def check_ollama():
    try:
        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            print("✅ Ollama server is running")
        else:
            print(f"⚠️ Ollama server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server NOT reachable. Is 'ollama serve' running?")
        print("   If you have the desktop app, make sure it's open.")
        return False

    # Check for model
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama3.2" in result.stdout:
            print("✅ Model 'llama3.2' found")
        else:
            print("❌ Model 'llama3.2' NOT found in Ollama list.")
            print("   Run: ollama pull llama3.2")
    except FileNotFoundError:
        print("❌ 'ollama' command not found in PATH.")

    return True

if __name__ == "__main__":
    print("🔍 Checking System Setup for AI Activity Tracker POC...\n")
    check_python()
    ocr_ok = check_tesseract()
    ai_ok = check_ollama()
    
    print("\n" + "="*40)
    if ocr_ok and ai_ok:
        print("🚀 System checks passed! You can run 'py main.py'")
    else:
        print("⚠️ Some checks failed. Please fix them before running.")
