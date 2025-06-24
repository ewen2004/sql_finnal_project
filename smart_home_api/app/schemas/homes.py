from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class HomeBase(BaseModel):
    home_name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = None
    square_meters: float = Field(..., gt=0)
    num_rooms: int = Field(..., gt=0)

class HomeCreate(HomeBase):
    user_id: int

class HomeUpdate(BaseModel):
    home_name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = None
    square_meters: Optional[float] = Field(None, gt=0)
    num_rooms: Optional[int] = Field(None, gt=0)

class HomeInDB(HomeBase):
    home_id: int
    user_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class Home(HomeInDB):
    pass
