from collections import Counter
import re

class TaskClassifier:
    def __init__(self):
        self.tasks = Counter()  # task_name -> usage_count (each count = 5 mins)
        
    def _get_keywords(self, text):
        # Basic tokenization: lowercase, remove non-alphanumeric, split
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'and', 'or', 'but', 'so', 'yet', 'nor', 'not', 'no'}
        return set([w for w in words if w not in stop_words])

    def classify_and_group(self, highlight):
        if not highlight or highlight == "No text detected - likely idle or screen capture failed.":
            return "Idle / System"

        current_keywords = self._get_keywords(highlight)
        best_match = None
        max_overlap = 0

        # Check against existing tasks
        for task_name in self.tasks:
            task_keywords = self._get_keywords(task_name)
            if not task_keywords:
                continue
            
            # Simple Jaccard index
            intersection = len(current_keywords.intersection(task_keywords))
            union = len(current_keywords.union(task_keywords))
            
            if union > 0:
                score = intersection / union
                if score > 0.2 and score > max_overlap: # Low threshold for POC
                    max_overlap = score
                    best_match = task_name

        if best_match:
            print(f"🧠 Task merged with existing: '{best_match}'")
            return best_match
        else:
            print(f"✨ New task created: '{highlight}'")
            return highlight

    def add_activity(self, highlight):
        group_name = self.classify_and_group(highlight)
        self.tasks[group_name] += 5 # Assume 5 min intervals
        return group_name
    
    def get_summary(self):
        summary = "\nFINAL TASKS:\n"
        for task, minutes in self.tasks.most_common():
            summary += f"{task} — {minutes} mins\n"
        return summary
