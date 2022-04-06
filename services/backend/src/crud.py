from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, u_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, num:int = 100):
    return db.query(models.User).limit(num).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed = user.password + "that'stoohard"
    db_user = models.User(email=user.email, username=user.username, hashed_password=fake_hashed)