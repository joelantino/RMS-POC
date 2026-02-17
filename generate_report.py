from collections import Counter
import re
import matplotlib.pyplot as plt

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
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.title(f"Activity Breakdown (Total: {total_minutes} mins)")
    plt.tight_layout()
    chart_path = "activity_report.png"
    plt.savefig(chart_path)
    print(f"📊 Chart saved to {chart_path}")
    plt.show()

if __name__ == "__main__":
    print("Generating Activity Report...")
    tasks, total_mins = parse_logs()
    if total_mins > 0:
        print(f"Total Time Tracked: {total_mins} minutes")
        generate_chart(tasks, total_mins)
