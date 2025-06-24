from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceUsageBase(BaseModel):
    device_id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    operation_type: Optional[str] = None
    operation_value: Optional[str] = None

class DeviceUsageCreate(DeviceUsageBase):
    pass

class DeviceUsageUpdate(BaseModel):
    end_time: Optional[datetime] = None
    operation_type: Optional[str] = None
    operation_value: Optional[str] = None

class DeviceUsageInDB(DeviceUsageBase):
    usage_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class DeviceUsage(DeviceUsageInDB):
    pass
