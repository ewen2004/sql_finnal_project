from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import device_usage as models
from ..schemas import device_usage as schemas
from ..services import device_usage as service
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.DeviceUsage, status_code=status.HTTP_201_CREATED)
def create_device_usage(device_usage: schemas.DeviceUsageCreate, db: Session = Depends(get_db)):
    return service.create_device_usage(db=db, device_usage=device_usage)

@router.get("/", response_model=List[schemas.DeviceUsage])
def read_device_usages(
    skip: int = 0, 
    limit: int = 100, 
    device_id: int = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    device_usages = service.get_device_usages(
        db, skip=skip, limit=limit, device_id=device_id, user_id=user_id
    )
    return device_usages

@router.get("/{usage_id}", response_model=schemas.DeviceUsage)
def read_device_usage(usage_id: int, db: Session = Depends(get_db)):
    db_device_usage = service.get_device_usage(db, usage_id=usage_id)
    if db_device_usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return db_device_usage

@router.put("/{usage_id}", response_model=schemas.DeviceUsage)
def update_device_usage(usage_id: int, device_usage: schemas.DeviceUsageUpdate, db: Session = Depends(get_db)):
    db_device_usage = service.get_device_usage(db, usage_id=usage_id)
    if db_device_usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return service.update_device_usage(db=db, usage_id=usage_id, device_usage=device_usage)

@router.delete("/{usage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_usage(usage_id: int, db: Session = Depends(get_db)):
    db_device_usage = service.get_device_usage(db, usage_id=usage_id)
    if db_device_usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    service.delete_device_usage(db=db, usage_id=usage_id)
    return {"ok": True}

@router.post("/{device_id}/start", response_model=schemas.DeviceUsage)
def start_device_usage(device_id: int, user_id: int, operation_type: str = None, db: Session = Depends(get_db)):
    return service.start_device_usage(db=db, device_id=device_id, user_id=user_id, operation_type=operation_type)

@router.post("/{device_id}/stop", response_model=schemas.DeviceUsage)
def stop_device_usage(device_id: int, operation_value: str = None, db: Session = Depends(get_db)):
    return service.stop_device_usage(db=db, device_id=device_id, operation_value=operation_value)
