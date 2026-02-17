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
        Analyze the following person's activity logs and group them into 'Main Tasks' (high-level categories like 'Programming', 'Communication', 'Meetings', 'Research').
        
        Provide the result as a JSON object where the key is the Activity from the log and the value is the Main Task it belongs to.
        Example:
        {{
            "Writing Python code for OCR": "Software Development",
            "Replying to client emails": "Communication"
        }}

        Activities:
        {logs_text}

        JSON Response Only:
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }

        try:
            print("🧠 AI is grouping activities into Main Tasks...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result_json = response.json().get("response", "{}")
            mapping = json.loads(result_json)
            
            # Calculate time per main task
            main_task_summary = {}
            for activity, minutes in activities_with_counts.items():
                main_task = mapping.get(activity, "Miscellaneous")
                main_task_summary[main_task] = main_task_summary.get(main_task, 0) + minutes
            
            return main_task_summary

        except Exception as e:
            print(f"Error during analysis: {e}")
            # Fallback: Just return the raw activities as main tasks
            return {act: mins for act, mins in activities_with_counts.items()}

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
