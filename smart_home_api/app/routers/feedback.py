from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import feedback as models
from ..schemas import feedback as schemas
from ..services import feedback as service

router = APIRouter()

@router.post("/", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return service.create_feedback(db=db, feedback=feedback)

@router.get("/", response_model=List[schemas.Feedback])
def read_feedbacks(
    skip: int = 0, 
    limit: int = 100, 
    user_id: int = None,
    feedback_type: str = None,
    db: Session = Depends(get_db)
):
    feedbacks = service.get_feedbacks(
        db, skip=skip, limit=limit, user_id=user_id, feedback_type=feedback_type
    )
    return feedbacks

@router.get("/{feedback_id}", response_model=schemas.Feedback)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = service.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return db_feedback

@router.put("/{feedback_id}", response_model=schemas.Feedback)
def update_feedback(feedback_id: int, feedback: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    db_feedback = service.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return service.update_feedback(db=db, feedback_id=feedback_id, feedback=feedback)

@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = service.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    service.delete_feedback(db=db, feedback_id=feedback_id)
    return {"ok": True}

@router.post("/{feedback_id}/respond", response_model=schemas.Feedback)
def respond_to_feedback(feedback_id: int, response: schemas.FeedbackResponse, db: Session = Depends(get_db)):
    db_feedback = service.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return service.respond_to_feedback(db=db, feedback_id=feedback_id, response=response)
