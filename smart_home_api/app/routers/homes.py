from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import homes as models
from ..schemas import homes as schemas
from ..services import homes as service

router = APIRouter()

@router.post("/", response_model=schemas.Home, status_code=status.HTTP_201_CREATED)
def create_home(home: schemas.HomeCreate, db: Session = Depends(get_db)):
    return service.create_home(db=db, home=home)

@router.get("/", response_model=List[schemas.Home])
def read_homes(skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)):
    homes = service.get_homes(db, skip=skip, limit=limit, user_id=user_id)
    return homes

@router.get("/{home_id}", response_model=schemas.Home)
def read_home(home_id: int, db: Session = Depends(get_db)):
    db_home = service.get_home(db, home_id=home_id)
    if db_home is None:
        raise HTTPException(status_code=404, detail="住宅不存在")
    return db_home

@router.put("/{home_id}", response_model=schemas.Home)
def update_home(home_id: int, home: schemas.HomeUpdate, db: Session = Depends(get_db)):
    db_home = service.get_home(db, home_id=home_id)
    if db_home is None:
        raise HTTPException(status_code=404, detail="住宅不存在")
    return service.update_home(db=db, home_id=home_id, home=home)

@router.delete("/{home_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_home(home_id: int, db: Session = Depends(get_db)):
    db_home = service.get_home(db, home_id=home_id)
    if db_home is None:
        raise HTTPException(status_code=404, detail="住宅不存在")
    service.delete_home(db=db, home_id=home_id)
    return {"ok": True}
