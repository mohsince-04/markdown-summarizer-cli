This project is a **local AI-powered CLI (Command Line Interface) tool** designed to analyze and query Markdown documents stored on your computer using Google's Gemini API.

![Summary](https://github.com/user-attachments/assets/a9add8cd-f855-4fb7-a1c4-11bd107e158b "Note: Ignore vepython, it's just an alias.")

### What it Does

1. **Document & Directory Summarization (`summarize`)**
* Takes a single Markdown file (`.md`) or scans an entire folder recursively for Markdown files.
* Combines the content and uses Gemini to generate a structured report featuring:
* A clear document title
* A single-sentence high-level summary
* 3 to 5 key bullet points (takeaways)
* Extracted topic tags


* Renders the summary nicely in your terminal using rich panels and colored text.


2. **Context-Grounded Q&A (`ask`)**
* Lets you ask specific questions (`-q / --query`) about your local notes or document sets.
* Restricts Gemini to answer **strictly based on the document text** provided (preventing outside hallucinations).
* Returns:
* A direct answer
* A calculated confidence score (0–100%)
* Supporting verbatim quotes directly extracted from your text.





---

### How the Code is Structured

```
            [main.py]           ──►                 [llm_service.py]         ──►              [schemas.py]
         CLI Interface &                           Gemini API Calls &                         Pydantic Data
        Text File Loader                           Prompt Processing                         Structure Models

```

* **`schemas.py`**: Defines the target data structures (`DocumentSummary` and `QAAnswer`) using Pydantic. This guarantees that Gemini returns structured, valid data instead of messy free-form text.
* **`llm_service.py`**: Interacts with the `google-genai` SDK using `gemini-2.5-flash`. It sets low temperatures for deterministic results and enforces the Pydantic schemas on API responses.
* **`main.py`**: The entry point built with **Typer** (for parsing arguments and flags) and **Rich** (for progress spinners, colors, and framed text boxes). It reads local Markdown files and presents the results.
