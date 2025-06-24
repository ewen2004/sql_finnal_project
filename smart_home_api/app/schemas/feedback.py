from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    user_id: int
    feedback_type: str  # 'bug', 'feature', 'general', 'support'
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5)

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class FeedbackResponse(BaseModel):
    response: str

class Feedback(FeedbackBase):
    feedback_id: int
    created_at: datetime
    responded: bool = False
    response: Optional[str] = None
    response_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True
