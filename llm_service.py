import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import DocumentSummary, QAAnswer

load_dotenv()


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Export it in your shell or set it in .env"
        )
    return genai.Client(api_key=api_key)


def generate_summary(text_content: str) -> DocumentSummary:
    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Analyze and extract key information from this document:\n\n{text_content}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DocumentSummary,
            temperature=0.2,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )
    return DocumentSummary.model_validate_json(response.text)


def ask_question(text_content: str, question: str) -> QAAnswer:
    client = get_client()
    prompt = f"Document Context:\n{text_content}\n\nQuestion: {question}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="Answer questions strictly based on the provided document context. If context is insufficient, state that clearly.",
            response_mime_type="application/json",
            response_schema=QAAnswer,
            temperature=0.1,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )
    return QAAnswer.model_validate_json(response.text)
