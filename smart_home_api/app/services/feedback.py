from sqlalchemy.orm import Session
from ..models.feedback import Feedback
from ..schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from datetime import datetime

def get_feedback(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.feedback_id == feedback_id).first()

def get_feedbacks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    user_id: int = None,
    feedback_type: str = None
):
    query = db.query(Feedback)
    
    if user_id is not None:
        query = query.filter(Feedback.user_id == user_id)
    
    if feedback_type is not None:
        query = query.filter(Feedback.feedback_type == feedback_type)
    
    return query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()

def create_feedback(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(
        user_id=feedback.user_id,
        feedback_type=feedback.feedback_type,
        content=feedback.content,
        rating=feedback.rating
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: int, feedback: FeedbackUpdate):
    db_feedback = get_feedback(db, feedback_id)
    
    update_data = feedback.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int):
    db_feedback = get_feedback(db, feedback_id)
    db.delete(db_feedback)
    db.commit()

def respond_to_feedback(db: Session, feedback_id: int, response: FeedbackResponse):
    """回复用户反馈"""
    db_feedback = get_feedback(db, feedback_id)
    
    db_feedback.response = response.response
    db_feedback.response_time = datetime.now()
    db_feedback.responded = True
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
