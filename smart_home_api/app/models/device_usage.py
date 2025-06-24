from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from ..database import Base

class DeviceUsage(Base):
    __tablename__ = "device_usage"
    
    usage_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    operation_type = Column(String(50))
    operation_value = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    device = relationship("Device", back_populates="usage_records")
    user = relationship("User")