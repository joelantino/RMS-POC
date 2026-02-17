import time
from datetime import datetime
import screenshot_capture
import ocr_processor
import ai_highlight_generator
from task_classifier import TaskClassifier
from task_analyzer import TaskAnalyzer
import cleanup_manager

def main():
    # Fresh Start: Check if it's a new day or if we should clear old data
    if cleanup_manager.should_reset_for_new_day():
        print("☀️ New day detected!")
        cleanup_manager.cleanup_session_data(delete_reports=True)

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
        
        # New Feature: AI-powered Main Task Analysis with Time Calculation
        print("\n🤖 Generating AI Structured Activity Report...")
        
        # Pass the task Counter directly to the analyzer
        if classifier.tasks:
            analyzer = TaskAnalyzer()
            main_task_summary = analyzer.analyze_and_group(dict(classifier.tasks))
            
            print("\n📋 FINAL ACTIVITY REPORT (BY MAIN TASK):")
            print("=" * 45)
            print(f"{'MAIN TASK':<30} | {'HOURS SPENT':<10}")
            print("-" * 45)
            
            report_text = "AI-STRUCTURED ACTIVITY ANALYSIS\n" + "=" * 45 + "\n"
            report_text += f"{'MAIN TASK':<30} | {'HOURS SPENT':<10}\n"
            report_text += "-" * 45 + "\n"
            
            for main_task, minutes in main_task_summary.items():
                hours = minutes / 60
                line = f"{main_task[:30]:<30} | {hours:.2f} hrs"
                print(line)
                report_text += line + "\n"
            
            print("=" * 45)
            
            # Save analysis to a separate file
            report_name = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_name, "w", encoding="utf-8") as f:
                f.write(report_text)
            print(f"✅ Final report saved to {report_name}")
            
            # Final Cleanup: Clear raw data but KEEP the one final report just generated
            cleanup_manager.cleanup_session_data(delete_reports=False)
            print("✅ Day data cleared. Ready for a fresh start next session!")

if __name__ == "__main__":
    main()
