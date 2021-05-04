from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, database, hashing, models
from sqlalchemy.orm import Session
from typing import List
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request=request, db=db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(database.get_db)):
    return user.get_all(db=db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_single_user(id, db: Session = Depends(database.get_db)):
    return user.get(id=id, db=db)


@router.delete('/{id}')
def delete_user(id, db: Session = Depends(database.get_db)):
    return user.delete(id=id, db=db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id, request: schemas.User, db: Session = Depends(database.get_db)):
    return user.update(id=id, request=request, db=db)
