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
        Analyzes activities to identify a single high-level 'Main Task' for the day
        and categorize sub-activities.
        """
        if not activities_with_counts:
            return {}

        activities_list = list(activities_with_counts.keys())
        logs_text = "\n".join([f"- {act}" for act in activities_list])

        prompt = f"""
        Instructions: 
        1. Identify the single most important 'Main Task' (Title) that describes the overall theme of these activities.
        2. Provide a brief 1-sentence summary of 'What this day was about'.
        3. Categorize each activity into: Software Development, Communication, Meetings, Research, Documentation, Administrative, or Miscellaneous.

        Format your response EXACTLY as follows:
        Main Task Title: [Dynamic Title here, e.g., Building OCR Module]
        Overall Summary: [One sentence description of all work done]
        ---
        Activity: [Activity Name] | Category: [Category Name]

        Activities to process:
        {logs_text}
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            print("🧠 AI is identifying your Main Task for the day...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            raw_text = response.json().get("response", "")
            
            # Extract Meta Info
            main_title = "General Work"
            overall_summary = "No summary generated."
            
            for line in raw_text.split('\n'):
                if line.startswith("Main Task Title:"):
                    main_title = line.replace("Main Task Title:", "").strip()
                elif line.startswith("Overall Summary:"):
                    overall_summary = line.replace("Overall Summary:", "").strip()

            # Sum up time per category
            category_summary = {}
            for activity, minutes in activities_with_counts.items():
                found_category = "Miscellaneous"
                for line in raw_text.split('\n'):
                    if activity.lower() in line.lower() and "Category:" in line:
                        parts = line.split("Category:")
                        if len(parts) > 1:
                            found_category = parts[1].strip()
                            break
                category_summary[found_category] = category_summary.get(found_category, 0) + minutes
            
            return {
                "title": main_title,
                "summary": overall_summary,
                "breakdown": category_summary
            }

        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return {
                "title": "Daily Activity",
                "summary": "Error during summarization.",
                "breakdown": {"Uncategorized": sum(activities_with_counts.values())}
            }

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
