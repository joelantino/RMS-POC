from collections import Counter
import re
import matplotlib.pyplot as plt
from task_analyzer import TaskAnalyzer
from datetime import datetime

def parse_logs(logfile="activity_log.txt"):
    tasks = Counter()
    total_minutes = 0

    try:
        with open(logfile, 'r', encoding='utf-8') as f:
            for line in f:
                # Basic parsing: assumes format [DATE TIME] Task: Group Name | Highlight: ...
                match = re.search(r"Task:\s(.*?)\s\|", line)
                if match:
                    group = match.group(1).strip()
                    tasks[group] += 5 # Each entry is 5 mins
                    total_minutes += 5
    except FileNotFoundError:
        print("No log file found. Run the tracker first!")
        return {}, 0

    return tasks, total_minutes

def generate_ai_report(tasks):
    if not tasks:
        print("No tasks found to analyze.")
        return

    print("\n🤖 Generating AI Structured Activity Report...")
    analyzer = TaskAnalyzer()
    main_task_summary = analyzer.analyze_and_group(dict(tasks))
    
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

def generate_chart(tasks, total_minutes):
    if not tasks:
        print("No data to visualize.")
        return

    labels = list(tasks.keys())
    sizes = list(tasks.values())
    
    # Sort for better visual
    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes, labels = zip(*sorted_pairs)

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    
    plt.title(f"Activity Breakdown (Total: {total_minutes} mins)")
    plt.tight_layout()
    chart_path = "activity_report.png"
    plt.savefig(chart_path)
    print(f"📊 Chart saved to {chart_path}")
    # plt.show() # Disabled for non-interactive environments

if __name__ == "__main__":
    print("Generating Activity Report...")
    tasks, total_mins = parse_logs()
    if total_mins > 0:
        print(f"Total Time Tracked: {total_mins} minutes")
        generate_ai_report(tasks)
        # generate_chart(tasks, total_mins) # Optional chart
