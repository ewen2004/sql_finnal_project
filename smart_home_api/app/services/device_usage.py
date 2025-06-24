from sqlalchemy.orm import Session
from ..models.device_usage import DeviceUsage
from ..schemas.device_usage import DeviceUsageCreate, DeviceUsageUpdate
from datetime import datetime

def get_device_usage(db: Session, usage_id: int):
    return db.query(DeviceUsage).filter(DeviceUsage.usage_id == usage_id).first()

def get_device_usages(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    device_id: int = None,
    user_id: int = None
):
    query = db.query(DeviceUsage)
    
    if device_id is not None:
        query = query.filter(DeviceUsage.device_id == device_id)
    
    if user_id is not None:
        query = query.filter(DeviceUsage.user_id == user_id)
    
    return query.order_by(DeviceUsage.start_time.desc()).offset(skip).limit(limit).all()

def create_device_usage(db: Session, device_usage: DeviceUsageCreate):
    db_device_usage = DeviceUsage(
        device_id=device_usage.device_id,
        user_id=device_usage.user_id,
        start_time=device_usage.start_time,
        end_time=device_usage.end_time,
        operation_type=device_usage.operation_type,
        operation_value=device_usage.operation_value
    )
    db.add(db_device_usage)
    db.commit()
    db.refresh(db_device_usage)
    return db_device_usage

def update_device_usage(db: Session, usage_id: int, device_usage: DeviceUsageUpdate):
    db_device_usage = get_device_usage(db, usage_id)
    
    update_data = device_usage.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_device_usage, key, value)
    
    db.commit()
    db.refresh(db_device_usage)
    return db_device_usage

def delete_device_usage(db: Session, usage_id: int):
    db_device_usage = get_device_usage(db, usage_id)
    db.delete(db_device_usage)
    db.commit()

def start_device_usage(db: Session, device_id: int, user_id: int, operation_type: str = None):
    """记录设备开始使用"""
    db_device_usage = DeviceUsage(
        device_id=device_id,
        user_id=user_id,
        start_time=datetime.now(),
        operation_type=operation_type
    )
    db.add(db_device_usage)
    db.commit()
    db.refresh(db_device_usage)
    return db_device_usage

def stop_device_usage(db: Session, device_id: int, operation_value: str = None):
    """记录设备停止使用"""
    # 查找该设备最近一条未结束的使用记录
    db_device_usage = (
        db.query(DeviceUsage)
        .filter(DeviceUsage.device_id == device_id, DeviceUsage.end_time.is_(None))
        .order_by(DeviceUsage.start_time.desc())
        .first()
    )
    
    if db_device_usage:
        db_device_usage.end_time = datetime.now()
        if operation_value:
            db_device_usage.operation_value = operation_value
        db.commit()
        db.refresh(db_device_usage)
    
    return db_device_usage
