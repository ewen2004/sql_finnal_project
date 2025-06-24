from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SecurityEventBase(BaseModel):
    home_id: int
    event_type: str
    description: str
    severity: str = "medium"  # low, medium, high, critical
    location: Optional[str] = None
    device_id: Optional[int] = None

class SecurityEventCreate(SecurityEventBase):
    event_time: Optional[datetime] = None

class SecurityEventUpdate(BaseModel):
    description: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None
    resolved: Optional[bool] = None
    resolution_notes: Optional[str] = None

class SecurityEventResolution(BaseModel):
    resolution_notes: str

class SecurityEvent(SecurityEventBase):
    event_id: int
    event_time: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
