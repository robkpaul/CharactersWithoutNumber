from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

initial_time = datetime.now()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    uptime = datetime.now()-initial_time
    return "Uptime: " + str(uptime)

@app.get("/userlist/", response_model=list[schemas.Character])
def list_users(limit: int=100, db: Session=Depends(get_db)):
    return crud.get_users(db, limit)

@app.post("/new_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if(db_user):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)