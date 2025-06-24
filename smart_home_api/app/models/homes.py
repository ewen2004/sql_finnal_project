from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Home(Base):
    __tablename__ = "homes"
    
    home_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    home_name = Column(String(100), nullable=False)
    address = Column(String(255))
    square_meters = Column(Float, nullable=False)
    num_rooms = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", backref="homes")
    devices = relationship("Device", back_populates="home")