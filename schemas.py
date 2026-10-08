from pydantic import BaseModel, Field
from typing import List


class DocumentSummary(BaseModel):
    title: str = Field(description="A concise, descriptive title for the document")
    one_sentence_summary: str = Field(description="A 1-sentence high-level summary")
    key_takeaways: List[str] = Field(
        description="3 to 5 key bullet points summarizing the document"
    )
    topics: List[str] = Field(description="Main topic tags extracted from the content")


class QAAnswer(BaseModel):
    question: str = Field(description="The user's original question")
    answer: str = Field(
        description="Direct, concise answer based on the provided document context"
    )
    confidence_score: float = Field(
        description="Confidence score between 0.0 and 1.0 based on context availability"
    )
    relevant_quotes: List[str] = Field(
        description="Exact quotes from the text supporting the answer"
    )
