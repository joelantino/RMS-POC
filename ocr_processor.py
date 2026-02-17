import pytesseract
from PIL import Image
import os
import shutil

# Try to find tesseract executable if not in PATH
tesseract_cmd = shutil.which("tesseract")
if not tesseract_cmd:
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{os.getlogin()}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Error: Image {image_path} not found.")
            return ""

        text = pytesseract.image_to_string(Image.open(image_path))
        
        # Basic cleaning (remove excessive newlines/spaces)
        cleaned_text = " ".join(text.split())
        
        print(f"🧾 OCR extracted {len(cleaned_text)} characters.")
        return cleaned_text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

if __name__ == "__main__":
    # Test stub
    pass
