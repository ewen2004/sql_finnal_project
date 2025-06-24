from sqlalchemy.orm import Session
from ..models.devices import Device, DeviceCategory
from ..schemas.devices import DeviceCreate, DeviceUpdate, DeviceCategoryCreate

def get_device_category(db: Session, category_id: int):
    return db.query(DeviceCategory).filter(DeviceCategory.category_id == category_id).first()

def get_device_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeviceCategory).offset(skip).limit(limit).all()

def create_device_category(db: Session, category: DeviceCategoryCreate):
    db_category = DeviceCategory(
        category_name=category.category_name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.device_id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100, home_id: int = None, category_id: int = None):
    query = db.query(Device)
    
    if home_id is not None:
        query = query.filter(Device.home_id == home_id)
    
    if category_id is not None:
        query = query.filter(Device.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()

def create_device(db: Session, device: DeviceCreate):
    db_device = Device(
        home_id=device.home_id,
        category_id=device.category_id,
        device_name=device.device_name,
        model=device.model,
        manufacturer=device.manufacturer,
        room_location=device.room_location,
        ip_address=device.ip_address,
        mac_address=device.mac_address,
        firmware_version=device.firmware_version,
        status=device.status
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device_id: int, device: DeviceUpdate):
    db_device = get_device(db, device_id)
    
    update_data = device.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    db_device = get_device(db, device_id)
    db.delete(db_device)
    db.commit()
