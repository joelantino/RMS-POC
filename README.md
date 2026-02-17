# AI Activity Tracker POC

This is a Proof-of-Concept for an AI-powered activity tracker that captures your screen, extracts text, uses AI to summarize your activity, and groups similar tasks.

## Setup

1.  **Install Python Dependencies:**
    Run this command in your terminal:
    ```bash
    py -m pip install -r requirements.txt
    ```
    *(Note: If `py` command is not found, try `python -m pip` instead)*

2.  **Install Tesseract OCR:**
    - Download and install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
    - Ensure `tesseract.exe` is in your PATH or installed in `C:\Program Files\Tesseract-OCR`.
    - **Verify installation:** Run `where tesseract` in terminal.

3.  **Install & Run Ollama:**
    - Download Ollama: https://ollama.com/
    - Pull the required model:
      ```bash
      ollama pull llama3.2
      ```
    - Ensure Ollama is running (`ollama serve`).

## Usage

Run the main script:

```bash
py main.py
```

The script will:
1.  Take a screenshot.
2.  Extract text using OCR.
3.  Send text to local AI model to generate a highlight.
4.  Group the task.
5.  Wait 5 minutes (standard) or adjusted interval.
6.  Repeat.

## Configuration

Edit `main.py` to change the capture interval:
```python
INTERVAL_SECONDS = 300 # 5 minutes
# INTERVAL_SECONDS = 10 # Testing mode
```
