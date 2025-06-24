from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import security_events as models
from ..schemas import security_events as schemas
from ..services import security_events as service
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.SecurityEvent, status_code=status.HTTP_201_CREATED)
def create_security_event(security_event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    return service.create_security_event(db=db, security_event=security_event)

@router.get("/", response_model=List[schemas.SecurityEvent])
def read_security_events(
    skip: int = 0, 
    limit: int = 100, 
    home_id: int = None,
    event_type: str = None,
    severity: str = None,
    db: Session = Depends(get_db)
):
    security_events = service.get_security_events(
        db, skip=skip, limit=limit, home_id=home_id, 
        event_type=event_type, severity=severity
    )
    return security_events

@router.get("/{event_id}", response_model=schemas.SecurityEvent)
def read_security_event(event_id: int, db: Session = Depends(get_db)):
    db_security_event = service.get_security_event(db, event_id=event_id)
    if db_security_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    return db_security_event

@router.put("/{event_id}", response_model=schemas.SecurityEvent)
def update_security_event(event_id: int, security_event: schemas.SecurityEventUpdate, db: Session = Depends(get_db)):
    db_security_event = service.get_security_event(db, event_id=event_id)
    if db_security_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    return service.update_security_event(db=db, event_id=event_id, security_event=security_event)

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_security_event(event_id: int, db: Session = Depends(get_db)):
    db_security_event = service.get_security_event(db, event_id=event_id)
    if db_security_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    service.delete_security_event(db=db, event_id=event_id)
    return {"ok": True}

@router.post("/{event_id}/resolve", response_model=schemas.SecurityEvent)
def resolve_security_event(event_id: int, resolution: schemas.SecurityEventResolution, db: Session = Depends(get_db)):
    db_security_event = service.get_security_event(db, event_id=event_id)
    if db_security_event is None:
        raise HTTPException(status_code=404, detail="安防事件不存在")
    return service.resolve_security_event(db=db, event_id=event_id, resolution=resolution)
