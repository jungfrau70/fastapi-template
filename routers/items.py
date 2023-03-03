# from database import engine, get_db
# from datetime import datetime
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, UploadFile, File
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.encoders import jsonable_encoder
# from typing import List
# from schemas import ItemIn, ItemOut
# from models import Item, User
# from routers.login import oauth2_scheme
# from jose import jwt
# from config import setting

# router = APIRouter(
#     prefix="/items",
#     tags=['Items']
# )

# def get_user_from_token(token, db):
#     try:
#         payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
#         user = db.query(User).filter(User.email==username).first()
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")            
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
#     return user

# @router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=ItemOut) 
# def create_item(item: ItemIn, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
#     # print(**item.dict())
#     user = get_user_from_token(token, db)
#     date_posted = datetime.now()
#     db_item = Item(**item.dict(), date_posted=date_posted, owner_id=user.id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# @router.get('/all', response_model=List[ItemOut])
# def get_items(db: Session = Depends(get_db)):
#     return db.query(Item).all()

# @router.get('/me', status_code=status.HTTP_200_OK, response_model=List[ItemOut])
# def get_my_items(db: Session = Depends(get_db)):
#     owner_id = 2
#     record = db.query(Item).filter(Item.owner_id == owner_id).all()
#     print(record)
#     if not record:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"record with the id {id} is not available")
#     return record  

# @router.get('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ItemOut) 
# def retrieve_by_id(id: int, db: Session = Depends(get_db)):
#     record = db.query(Item).filter(Item.id == id).first()
#     # print(record, type(record))
#     if not record:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"record with the id {id} does not exists")
#     return record  
    
# # Method-1
# @router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update_by_id(id: int, request: ItemIn, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
#     user = get_user_from_token(token, db)       
#     record = db.query(Item).filter(Item.id == id)
#     if not record.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with the id {id} does not exists")
#     if record.first().owner_id == user.id:    
#         record.update(jsonable_encoder(request))
#         db.commit()
#         return {"message": f"Details for Item ID {id} has been successfully updated"}
#     else:        
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                         detail="You are not authorized")  
# # Method-2
# @router.put('/update1/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update_by_id(id: int, request: ItemIn, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
#     user = get_user_from_token(token, db)    
#     record  = db.query(Item).filter(Item.id == id)
#     if not record.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with the id {id} does not exists")
#     if record.first().owner_id == user.id:    
#         record.update(request.__dict__)
#         db.commit()
#         return {"message": f"Details for Item ID {id} has been successfully updated"}
#     else:        
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                         detail="You are not authorized")  
    
# @router.delete('/delete/{id}', status_code=status.HTTP_202_ACCEPTED)
# def delete_by_id(id: int, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
#     user = get_user_from_token(token, db)
#     record  = db.query(Item).filter(Item.id == id)
#     if not record.first():
#         return {"message": f"No details exists for Item ID {id}"}    
#     if record.first().owner_id == user.id:
#         record.delete()
#         db.commit()
#         return {"message": f"Details for Item ID {id} has been successfully deleted"}        
#     else:        
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                         detail="You are not authorized")  

