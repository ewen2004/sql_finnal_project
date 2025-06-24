from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DeviceCategoryBase(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class DeviceCategoryCreate(DeviceCategoryBase):
    pass

class DeviceCategoryInDB(DeviceCategoryBase):
    category_id: int

    class Config:
         from_attributes = True

class DeviceCategory(DeviceCategoryInDB):
    pass

class DeviceBase(BaseModel):
    device_name: str = Field(..., min_length=1, max_length=100)
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    room_location: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    firmware_version: Optional[str] = None
    status: str = "offline"

class DeviceCreate(DeviceBase):
    home_id: int
    category_id: int

class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    room_location: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    firmware_version: Optional[str] = None
    status: Optional[str] = None

class DeviceInDB(DeviceBase):
    device_id: int
    home_id: int
    category_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class Device(DeviceInDB):
    category: DeviceCategory

    class Config:
        from_attributes = True
