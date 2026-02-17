import requests
import json
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

class TaskAnalyzer:
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model = MODEL_NAME

    def analyze_and_group(self, activity_logs):
        """
        Analyzes a list of activities and groups them into 
        Main Tasks and Sub Tasks using AI.
        """
        if not activity_logs:
            return "No activities to analyze."

        # Combine logs into a text block for AI analysis
        logs_text = "\n".join([f"- {log}" for log in activity_logs])

        prompt = f"""
        Analyze the following person's daily activity logs. 
        Identify the 'Main Tasks' (high-level goals or categories) 
        and group the 'Sub Tasks' (specific actions) under them.
        
        Format the output as a clean hierarchical list:
        # Main Task 1
          - Sub Task A
          - Sub Task B
        # Main Task 2
          - Sub Task C

        Daily Logs:
        {logs_text}

        Response:
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            print("🧠 AI is analyzing and grouping tasks...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to Ollama. Ensure it's running locally."
        except Exception as e:
            return f"Error during analysis: {str(e)}"

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
