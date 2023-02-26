import schemas, models

from database import engine, get_db
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from schemas import ItemIn, ItemOut
from models import Item

router = APIRouter(
    prefix="/items",
    tags=['Items']
)

@router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=ItemOut) 
def create_(item: ItemIn, db: Session = Depends(get_db)):
    # print(**item.dict())
    date_posted = datetime.now()
    owner_id = 2
    db_item = Item(**item.dict(), date_posted=date_posted, owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get('/all', response_model=List[ItemOut])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.get('/me', status_code=status.HTTP_200_OK, response_model=List[ItemOut])
def get_my_items(db: Session = Depends(get_db)): 
    owner_id = 2
    record = db.query(Item).filter(Item.owner_id == owner_id).all()
    print(record)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} is not available")
    return record  

@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ItemOut) 
def retrieve_by_id(id: int, db: Session = Depends(get_db)):
    record = db.query(Item).filter(Item.id == id).first()
    # print(record, type(record))
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} does not exists")
    return record  
    
# Method-1
@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id: int, request: ItemIn, db: Session = Depends(get_db)):
    record = db.query(Item).filter(Item.id == id)
    if not record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} does not exists")
    record.update(jsonable_encoder(request))
    db.commit()
    return {"message": f"Details for Item ID {id} has been successfully updated"}

# Method-2
@router.put('/update1/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id: int, request: ItemIn, db: Session = Depends(get_db)):
    record  = db.query(Item).filter(Item.id == id)
    if not record.first():
        return {"message": f"No details exists for Item ID {id}"}
    record.update(request.__dict__)
    db.commit()
    return {"message": f"Details for Item ID {id} has been successfully updated"}

@router.delete('/delete/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    record  = db.query(Item).filter(Item.id == id)
    if not record.first():
        return {"message": f"No details exists for Item ID {id}"}
    record.delete()
    db.commit()
    return {"message": f"Details for Item ID {id} has been successfully deleted"}