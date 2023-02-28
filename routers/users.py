from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List
from hashing import Hasher
from schemas import UserIn, UserOut
from models import User
from routers.login import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=UserOut) 
def create_user(user: UserIn, db: Session = Depends(get_db)):#, token:str=Depends(oauth2_scheme)): 
    db_user = User(email=user.email, hashed_password=Hasher.get_hash_password(user.password), name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_email(db: Session = Depends(get_db)): 
    email = "user1@example.com"
    record = db.query(User).filter(User.email == email).first()
    print(record)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} is not available")
    return record  

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    record = db.query(User).filter(User.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} is not available")
    return record  


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT) # ,current_user: schemas.User = Depends(oauth2.get_current_user)):
def destroy(id: int, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)): 
    record = db.query(User).filter(User.id == id)

    if not record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id {id} not found")

    # record.delete(synchronize_session=False)
    db.query(User).filter(User.id == id).delete()
    db.commit()
    return 'done'
