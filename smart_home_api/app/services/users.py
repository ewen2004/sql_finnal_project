from sqlalchemy.orm import Session
from ..models.users import User
from ..schemas.users import UserCreate, UserUpdate
from datetime import datetime
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password.decode('utf-8'),
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    
    update_data = user.dict(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = bcrypt.hashpw(update_data["password"].encode('utf-8'), bcrypt.gensalt())
        update_data["password_hash"] = hashed_password.decode('utf-8')
        del update_data["password"]
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    
def update_last_login(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db_user.last_login = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
