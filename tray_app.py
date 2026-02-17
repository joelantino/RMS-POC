import os
import time
import threading
from datetime import datetime
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import screenshot_capture
import ocr_processor
import ai_highlight_generator
from task_classifier import TaskClassifier
from task_analyzer import TaskAnalyzer
import cleanup_manager
import subprocess

class ActivityTrackerTray:
    def __init__(self):
        self.is_running = False
        self.classifier = TaskClassifier()
        self.INTERVAL_SECONDS = 300 
        self.icon = None
        self.thread = None

    def create_image(self):
        # Generate a simple blue circle icon
        width = 64
        height = 64
        color1 = (0, 120, 215) # Windows Blue
        color2 = (255, 255, 255)
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=color2, outline=color2)
        return image

    def tracking_loop(self):
        print("🚀 Background Tracking Started...")
        while self.is_running:
            start_time = time.time()
            try:
                # 1. Capture Screenshot
                image_path = screenshot_capture.take_screenshot()
                
                # 2. Extract Text
                text = ocr_processor.extract_text(image_path)
                
                # Auto-Delete Screenshot
                if os.path.exists(image_path):
                    os.remove(image_path)
                
                if text.strip():
                    # 3. Generate Highlight
                    highlight = ai_highlight_generator.generate_highlight(text)
                    
                    # 4. Classify & Log
                    group_name = self.classifier.add_activity(highlight)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] Task: {group_name} | Highlight: {highlight}\n"
                    with open("activity_log.txt", "a", encoding="utf-8") as f:
                        f.write(log_entry)
            except Exception as e:
                print(f"Tracking error: {e}")

            # Wait for next interval
            elapsed = time.time() - start_time
            sleep_time = max(0, self.INTERVAL_SECONDS - elapsed)
            
            # Check for stop signal more frequently
            for _ in range(int(sleep_time)):
                if not self.is_running: break
                time.sleep(1)

    def on_start(self, icon, item):
        if not self.is_running:
            self.is_running = True
            # Check for new day/cleanup
            if cleanup_manager.should_reset_for_new_day():
                cleanup_manager.cleanup_session_data(delete_reports=True)
            
            self.thread = threading.Thread(target=self.tracking_loop, daemon=True)
            self.thread.start()
            self.icon.title = "AI Tracker: ACTIVE"
            self.icon.update_menu()

    def on_stop(self, icon, item):
        if self.is_running:
            self.is_running = False
            self.icon.title = "AI Tracker: IDLE"
            self.generate_final_report()
            self.icon.update_menu()

    def generate_final_report(self):
        if not self.classifier.tasks:
            return
            
        print("🤖 Generating Final AI Report...")
        analyzer = TaskAnalyzer()
        report_data = analyzer.analyze_and_group(dict(self.classifier.tasks))
        
        title = report_data.get("title", "Work Session")
        summary = report_data.get("summary", "")
        breakdown = report_data.get("breakdown", {})

        report_text = f"AI-STRUCTURED ACTIVITY ANALYSIS\n"
        report_text += f"MAIN THEME: {title}\n"
        report_text += f"WHAT HAPPENED: {summary}\n"
        report_text += "=" * 60 + "\n"
        report_text += f"{'CATEGORY':<30} | {'HOURS SPENT':<10}\n"
        report_text += "-" * 60 + "\n"
        
        for category, minutes in breakdown.items():
            hours = minutes / 60
            report_text += f"{category[:30]:<30} | {hours:.2f} hrs\n"
        
        report_name = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_name, "w", encoding="utf-8") as f:
            f.write(report_text)
            
        # Cleanup
        cleanup_manager.cleanup_session_data(delete_reports=False)
        
        # Auto-open the report for the user
        try:
            os.startfile(report_name)
        except:
            pass

    def on_exit(self, icon, item):
        self.on_stop(icon, item)
        self.icon.stop()

    def run(self):
        menu = (
            item('Start Tracking', self.on_start, enabled=lambda item: not self.is_running),
            item('Stop & Generate Report', self.on_stop, enabled=lambda item: self.is_running),
            item('Exit', self.on_exit)
        )
        self.icon = pystray.Icon("AI_Activity_Tracker", self.create_image(), "AI Activity Tracker", menu)
        self.icon.run()

if __name__ == "__main__":
    app = ActivityTrackerTray()
    app.run()
