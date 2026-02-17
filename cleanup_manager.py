import os
import shutil
import glob
from datetime import datetime

def cleanup_session_data(delete_reports=False):
    """
    Deletes screenshots and clears the activity log.
    Optionally deletes old final reports.
    """
    print("\n🧹 Initializing Data Cleanup...")

    # 1. Delete Screenshots
    if os.path.exists("screenshots"):
        files = glob.glob('screenshots/*')
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"Error deleting screenshot {f}: {e}")
        print("🗑️  All screenshots deleted.")

    # 2. Clear Activity Log
    if os.path.exists("activity_log.txt"):
        try:
            with open("activity_log.txt", "w") as f:
                f.truncate(0)
            print("🗑️  activity_log.txt cleared.")
        except Exception as e:
            print(f"Error clearing activity log: {e}")

    # 3. Delete old reports if requested
    if delete_reports:
        reports = glob.glob('final_report_*.txt') + glob.glob('analysis_report_*.txt')
        for r in reports:
            try:
                os.remove(r)
            except Exception as e:
                print(f"Error deleting report {r}: {e}")
        print("🗑️  Previous reports deleted.")

def should_reset_for_new_day():
    """
    Checks if the last activity was on a previous day.
    """
    if not os.path.exists("activity_log.txt") or os.stat("activity_log.txt").st_size == 0:
        return False
    
    try:
        with open("activity_log.txt", "r") as f:
            lines = f.readlines()
            if not lines:
                return False
            # Extract date from first line: [2026-02-16 14:33:10]
            last_line = lines[-1]
            if "[" in last_line and "]" in last_line:
                log_date_str = last_line.split("]")[0].strip("[")
                log_date = datetime.strptime(log_date_str, "%Y-%m-%d %H:%M:%S").date()
                if log_date < datetime.now().date():
                    return True
    except Exception:
        pass
    
    return False

if __name__ == "__main__":
    # Manual test
    cleanup_session_data(delete_reports=True)
