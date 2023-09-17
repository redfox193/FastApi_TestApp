from fastapi import Depends, APIRouter, HTTPException, Security
from sqlalchemy.orm import Session

from ..database import crud, models, schemas
from ..database.database import SessionLocal, engine
from .login import get_admin

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["database"], dependencies=[Depends(get_admin)])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.get_user_by_name(db, user_name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already taken")
    
    return crud.create_user(db=db, user=user)


@router.get("/users_database", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users_database/id-{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users_database/name-{user_name}", response_model=schemas.User)
def read_user_by_name(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user