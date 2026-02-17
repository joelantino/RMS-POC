import time
from datetime import datetime
import screenshot_capture
import ocr_processor
import ai_highlight_generator
from task_classifier import TaskClassifier

def main():
    print("🚀 Starting AI Activity Tracker POC...")
    print("Press Ctrl+C to stop.")
    
    classifier = TaskClassifier()
    
    # Configuration
    # INTERVAL_SECONDS = 300  # 5 minutes as requested
    # For testing/demo, uncomment below:
    # INTERVAL_SECONDS = 10 
    INTERVAL_SECONDS = 300 

    try:
        while True:
            start_time = time.time()
            
            # 1. Capture Screenshot
            image_path = screenshot_capture.take_screenshot()
            
            # 2. Extract Text via OCR
            print("Running OCR...")
            text = ocr_processor.extract_text(image_path)
            
            if not text.strip():
                print("⚠️ No text found in screenshot.")
                highlight = "Idle / Empty Screen"
            else:
                # 3. Generate AI Highlight
                print("Generating AI Highlight...")
                highlight = ai_highlight_generator.generate_highlight(text)
            
            # 4. Classify & Group Task
            group_name = classifier.add_activity(highlight)
            
            # Log to File
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Task: {group_name} | Highlight: {highlight}\n"
            with open("activity_log.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"📝 Logged to activity_log.txt")
            
            # 5. Print Summary
            print("-" * 30)
            print(classifier.get_summary())
            print("-" * 30)
            
            # Wait for next interval
            elapsed = time.time() - start_time
            sleep_time = max(0, INTERVAL_SECONDS - elapsed)
            print(f"Waiting {int(sleep_time)} seconds for next capture...")
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n🛑 Tracker stopped by user.")
        print(classifier.get_summary())

if __name__ == "__main__":
    main()
