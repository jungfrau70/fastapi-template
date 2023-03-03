# from fastapi import Depends, APIRouter, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from database import get_db
# from sqlalchemy.orm import Session
# from models import User
# from hashing import Hasher
# from jose import jwt
# from config import setting
# from schemas import UserIn, UserOut

# router = APIRouter(
#     prefix="/login",
#     tags=['Auths']
# )

# #oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token/")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

# @router.post("/token")
# def retrieve_token_after_authentication(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
#     print(form_data)
#     user = db.query(User).filter(User.email==form_data.username).first()
#     print(user)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
#     if not Hasher.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

#     data = { "sub": form_data.username}
#     jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

#     return  { "access_token" : jwt_token, "token_type" : 'bearer'}

# @router.post("/")
# def retrieve_token(request: UserIn, db: Session = Depends(get_db)):
#     print(request)
#     user = db.query(User).filter(User.email==request.email).first()
#     print(user)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
#     if not Hasher.verify_password(request.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

#     data = { "sub": request.email}
#     jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

#     return  { "access_token" : jwt_token, "token_type" : 'bearer'}


