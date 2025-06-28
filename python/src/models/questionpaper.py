from typing import Optional, List
from beanie import Document, Indexed
from pydantic import BaseModel, Field


class OptionSchema(BaseModel):
    A: Optional[str]
    B: Optional[str]
    C: Optional[str]
    D: Optional[str]
    E: Optional[str]


class QuestionSchema(BaseModel):
    number: int
    question: str
    options: OptionSchema
    answer: str


class QuestionBlockSchema(BaseModel):
    context: str
    questions: List[QuestionSchema]


class QuestionPaper(Document):
    originalFilename: str
    backendFilename: str
    total_questions: int
    question_blocks: List[QuestionBlockSchema]

class Settings:
        name = "questionpapers"  # collection name in MongoDB
    