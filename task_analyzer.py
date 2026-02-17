import requests
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class TaskAnalyzer:
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model = MODEL_NAME

    def analyze_and_group(self, activities_with_counts):
        """
        Analyzes activities and maps each to a 'Main Task'.
        Returns a dictionary mapping Main Task -> Total Minutes.
        """
        if not activities_with_counts:
            return {}

        activities_list = list(activities_with_counts.keys())
        logs_text = "\n".join([f"- {act}" for act in activities_list])

        prompt = f"""
        Instructions: Categorize each specific activity into one of these High-Level Categories:
        1. Software Development
        2. Communication
        3. Meetings
        4. Research & Learning
        5. Documentation
        6. Administrative
        7. Miscellaneous

        Return the result exactly in this format for every activity:
        Activity: [Activity Name] | Category: [Category Name]

        Activities to categorize:
        {logs_text}
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            print("🧠 AI is analyzing activities...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            raw_text = response.json().get("response", "")
            
            # Sum up time per category
            main_task_summary = {}
            
            # Process the text response line by line
            # Format: Activity: ... | Category: ...
            for activity, minutes in activities_with_counts.items():
                found_category = "Miscellaneous"
                # Look for the specific activity in the AI output
                for line in raw_text.split('\n'):
                    if activity.lower() in line.lower() and "Category:" in line:
                        parts = line.split("Category:")
                        if len(parts) > 1:
                            found_category = parts[1].strip()
                            break
                
                main_task_summary[found_category] = main_task_summary.get(found_category, 0) + minutes
            
            return main_task_summary

        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return {"Uncategorized": sum(activities_with_counts.values())}

if __name__ == "__main__":
    # Test with sample data
    test_logs = [
        "Take a screenshot, extract text using OCR",
        "Develop a reliable document intelligence system",
        "Schedule a meeting with Aruna",
        "Combine multiple AI models for efficiency",
        "Review and annotate a presentation",
        "Send and respond to emails"
    ]
    analyzer = TaskAnalyzer()
    print(analyzer.analyze_and_group(test_logs))
