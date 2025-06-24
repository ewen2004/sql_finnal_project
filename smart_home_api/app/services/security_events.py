from sqlalchemy.orm import Session
from ..models.security_events import SecurityEvent
from ..schemas.security_events import SecurityEventCreate, SecurityEventUpdate, SecurityEventResolution
from datetime import datetime

def get_security_event(db: Session, event_id: int):
    return db.query(SecurityEvent).filter(SecurityEvent.event_id == event_id).first()

def get_security_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    home_id: int = None,
    event_type: str = None,
    severity: str = None
):
    query = db.query(SecurityEvent)
    
    if home_id is not None:
        query = query.filter(SecurityEvent.home_id == home_id)
    
    if event_type is not None:
        query = query.filter(SecurityEvent.event_type == event_type)
    
    if severity is not None:
        query = query.filter(SecurityEvent.severity == severity)
    
    return query.order_by(SecurityEvent.event_time.desc()).offset(skip).limit(limit).all()

def create_security_event(db: Session, security_event: SecurityEventCreate):
    db_security_event = SecurityEvent(
        home_id=security_event.home_id,
        event_type=security_event.event_type,
        event_time=security_event.event_time or datetime.now(),
        description=security_event.description,
        severity=security_event.severity,
        location=security_event.location,
        device_id=security_event.device_id
    )
    db.add(db_security_event)
    db.commit()
    db.refresh(db_security_event)
    return db_security_event

def update_security_event(db: Session, event_id: int, security_event: SecurityEventUpdate):
    db_security_event = get_security_event(db, event_id)
    
    update_data = security_event.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_security_event, key, value)
    
    db.commit()
    db.refresh(db_security_event)
    return db_security_event

def delete_security_event(db: Session, event_id: int):
    db_security_event = get_security_event(db, event_id)
    db.delete(db_security_event)
    db.commit()

def resolve_security_event(db: Session, event_id: int, resolution: SecurityEventResolution):
    """解决安防事件"""
    db_security_event = get_security_event(db, event_id)
    
    db_security_event.resolved = True
    db_security_event.resolution_time = datetime.now()
    db_security_event.resolution_notes = resolution.resolution_notes
    
    db.commit()
    db.refresh(db_security_event)
    return db_security_event
