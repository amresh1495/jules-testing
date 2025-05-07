from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId

# Helper to validate ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    question_text: str
    solution: str
    next_revision_date: datetime
    current_interval_days: int = 0

    class Config:
        populate_by_name = True # Allow population by field name OR alias ('_id')
        arbitrary_types_allowed = True # Allow ObjectId
        json_encoders = {ObjectId: str} # How to encode ObjectId to JSON

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    solution: Optional[str] = None
    next_revision_date: Optional[datetime] = None
    current_interval_days: Optional[int] = None
