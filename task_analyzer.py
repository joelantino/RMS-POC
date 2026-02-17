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
        Analyzes activities by indexing them to ensure reliable AI categorization.
        Returns title, summary, and hourly breakdown.
        """
        if not activities_with_counts:
            return {}

        activities_list = list(activities_with_counts.keys())
        # Provide IDs to AI for reliable matching
        indexed_logs = "\n".join([f"ID_{i}: {act}" for i, act in enumerate(activities_list)])

        prompt = f"""
        Instructions: 
        1. Identify a high-level 'Main Task Title' (the project theme).
        2. Provide a 1-sentence 'Overall Summary' of the work.
        3. Categorize each activity ID into one of: Software Development, Communication, Meetings, Research, Documentation, Administrative, or Miscellaneous.

        Format your response EXACTLY as follows:
        Main Task Title: [Title]
        Overall Summary: [Summary]
        ---
        ID_0: [Category]
        ID_1: [Category]
        ... and so on for all IDs.

        Activities to process:
        {indexed_logs}
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            print("🧠 AI is analyzing and clubbing activities...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            raw_text = response.json().get("response", "")
            
            # Extract Meta Info
            main_title = "General Work"
            overall_summary = "No summary generated."
            
            # Map for ID -> Category
            id_to_category = {}
            
            for line in raw_text.split('\n'):
                line = line.strip()
                if line.startswith("Main Task Title:"):
                    main_title = line.replace("Main Task Title:", "").strip()
                elif line.startswith("Overall Summary:"):
                    overall_summary = line.replace("Overall Summary:", "").strip()
                elif "ID_" in line and ":" in line:
                    # Parse "ID_0: Category"
                    parts = line.split(":")
                    if len(parts) >= 2:
                        idx_str = parts[0].strip()
                        category = parts[1].strip().strip('[]')
                        id_to_category[idx_str] = category

            # Sum up time per category using the ID map
            category_summary = {}
            for i, activity in enumerate(activities_list):
                id_key = f"ID_{i}"
                found_category = id_to_category.get(id_key, "Miscellaneous")
                
                minutes = activities_with_counts[activity]
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
                "summary": "Error during analysis execution.",
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
