from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import devices as models
from ..schemas import devices as schemas
from ..services import devices as service

router = APIRouter()

# 设备类别API
@router.post("/categories/", response_model=schemas.DeviceCategory, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.DeviceCategoryCreate, db: Session = Depends(get_db)):
    return service.create_device_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.DeviceCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = service.get_device_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=schemas.DeviceCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = service.get_device_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="设备类别不存在")
    return db_category

# 设备API
# 例如在routers/devices.py中
@router.post("/", response_model=schemas.Device, status_code=status.HTTP_201_CREATED)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """
    创建新设备
    
    - **home_id**: 设备所属住宅ID
    - **category_id**: 设备类别ID
    - **device_name**: 设备名称
    - **model**: 设备型号（可选）
    - **manufacturer**: 设备制造商（可选）
    - **room_location**: 设备所在房间（可选）
    - **ip_address**: 设备IP地址（可选）
    - **mac_address**: 设备MAC地址（可选）
    - **firmware_version**: 固件版本（可选）
    - **status**: 设备状态，默认为"offline"
    """
    return service.create_device(db=db, device=device)

@router.get("/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, home_id: int = None, category_id: int = None, db: Session = Depends(get_db)):
    devices = service.get_devices(db, skip=skip, limit=limit, home_id=home_id, category_id=category_id)
    return devices

@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = service.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return db_device

@router.put("/{device_id}", response_model=schemas.Device)
def update_device(device_id: int, device: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    db_device = service.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return service.update_device(db=db, device_id=device_id, device=device)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = service.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    service.delete_device(db=db, device_id=device_id)
    return {"ok": True}
