import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def generate_highlight(ocr_text):
    if not ocr_text.strip():
        return "No text detected - likely idle or screen capture failed."

    prompt = f"""Summarize the following screen content into a single work activity description (max 10-15 words).
Do not include technical jargon if possible. Focus on the user's intent.
Example: Writing Python code for screenshot capture.
Text: {ocr_text[:1000]}... (truncated)"""
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        highlight = result.get("response", "").strip()
        print(f"🤖 AI Highlight: {highlight}")
        return highlight

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Is it running?")
        return "Ollama connection failed"
    except Exception as e:
        print(f"Error generating highlight: {e}")
        return "Error in AI processing"

if __name__ == "__main__":
    # Test stub
    pass
