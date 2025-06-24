from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    feedback_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    responded = Column(Boolean, default=False)
    response = Column(Text, nullable=True)
    response_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # 使用字符串引用防止循环导入
    user = relationship("User", back_populates="feedbacks")
