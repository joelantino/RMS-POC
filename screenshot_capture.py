import mss
import os
from datetime import datetime
from PIL import Image

def take_screenshot():
    # Ensure screenshots directory exists
    screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(screenshot_dir, f"{timestamp}.png")

    with mss.mss() as sct:
        # Capture the entire screen (monitor 1 by default)
        sct.shot(mon=-1, output=screenshot_path)
    
    print(f"📸 Screenshot captured: {screenshot_path}")
    return screenshot_path

if __name__ == "__main__":
    take_screenshot()
