from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class DeviceCategory(Base):
    __tablename__ = "device_categories"
    
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False)
    description = Column(String(255))
    
    # 关系
    devices = relationship("Device", back_populates="category")

class Device(Base):
    __tablename__ = "devices"
    
    device_id = Column(Integer, primary_key=True, index=True)
    home_id = Column(Integer, ForeignKey("homes.home_id"))
    category_id = Column(Integer, ForeignKey("device_categories.category_id"))
    device_name = Column(String(100), nullable=False)
    model = Column(String(100))
    manufacturer = Column(String(100))
    room_location = Column(String(50))
    ip_address = Column(String(20))
    mac_address = Column(String(20))
    firmware_version = Column(String(50))
    status = Column(String(20), default="offline")
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    home = relationship("Home", back_populates="devices")
    category = relationship("DeviceCategory", back_populates="devices")
    usage_records = relationship("DeviceUsage", back_populates="device")