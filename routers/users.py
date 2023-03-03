from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, status, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List
from hashing import Hasher
# from schemas import UserIn, UserOut
from models import User
# from routers.login import oauth2_scheme
from schemas import PostSchema, UserSchema, UserLoginSchema, UserOutSchema, TokenData
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from auth.auth_handler import get_current_user
from config import setting

ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

def check_user(data: UserLoginSchema, db):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return False
    return True

@router.post("/signup")
def create_user(user: UserSchema = Body(...), db: Session = Depends(get_db)):
    user = User(email=user.email, hashed_password=Hasher.get_hash_password(user.password), name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return signJWT(user.email)


@router.post("/login")
def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    if check_user(user, db):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

@router.get("/me", dependencies=[Depends(get_current_user)])
async def read_users_me():
    current_user = get_current_user
    return current_user

# @router.get("/me", response_model=UserOutSchema, dependencies=[Depends(get_current_user)])
# async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
#     return current_user

# @router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=UserOut) 
# def create_user(user: UserIn, db: Session = Depends(get_db)):#, token:str=Depends(oauth2_scheme)): 
#     db_user = User(email=user.email, hashed_password=Hasher.get_hash_password(user.password), name=user.name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.get('/all', status_code=status.HTTP_200_OK, response_model=List[UserOut])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(User).all()



# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT) # ,current_user: schemas.User = Depends(oauth2.get_current_user)):
# def destroy(id: int, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)): 
#     record = db.query(User).filter(User.id == id)

#     if not record.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"record with id {id} not found")

#     # record.delete(synchronize_session=False)
#     db.query(User).filter(User.id == id).delete()
#     db.commit()
#     return 'done'
