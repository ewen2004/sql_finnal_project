from sqlalchemy.orm import Session
from ..models.homes import Home
from ..schemas.homes import HomeCreate, HomeUpdate

def get_home(db: Session, home_id: int):
    return db.query(Home).filter(Home.home_id == home_id).first()

def get_homes(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(Home)
    
    if user_id is not None:
        query = query.filter(Home.user_id == user_id)
    
    return query.offset(skip).limit(limit).all()

def create_home(db: Session, home: HomeCreate):
    db_home = Home(
        user_id=home.user_id,
        home_name=home.home_name,
        address=home.address,
        square_meters=home.square_meters,
        num_rooms=home.num_rooms
    )
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

def update_home(db: Session, home_id: int, home: HomeUpdate):
    db_home = get_home(db, home_id)
    
    update_data = home.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_home, key, value)
    
    db.commit()
    db.refresh(db_home)
    return db_home

def delete_home(db: Session, home_id: int):
    db_home = get_home(db, home_id)
    db.delete(db_home)
    db.commit()
