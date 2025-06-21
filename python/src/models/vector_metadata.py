# models/vector_metadata.py

from typing import List, Optional
from beanie import Document
from pydantic import Field
from datetime import datetime


class QuestionVectorMetadata(Document):
    question_id: str                         # Mongo ID of the question
    paper_id: str                            # Parent paper
    global_number: int                       # Unique question number
    context: Optional[str]
    question: str
    options: dict
    answer: str

    difficulty: Optional[str] = None         # "easy", "medium", "hard"
    tags: Optional[List[str]] = []           # ["reasoning", "symbols"]
    cluster_id: Optional[str] = None         # e.g. "cluster_3"

    embedding_model: str = "multi-qa-mpnet-base-dot-v1"
    faiss_index: int                         # Index position in FAISS
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "question_vectors"
