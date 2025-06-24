from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, func
from sqlalchemy.orm import relationship
from ..database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    event_id = Column(Integer, primary_key=True, index=True)
    home_id = Column(Integer, ForeignKey("homes.home_id"))
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    event_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    description = Column(Text)
    location = Column(String(100), nullable=True)
    event_time = Column(DateTime, default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolved_by = Column(Integer, ForeignKey("users.user_id"))
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    home = relationship("Home")
    device = relationship("Device")
    resolver = relationship("User")
