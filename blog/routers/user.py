from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, database, hashing, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()



@router.post('/user', status_code=status.HTTP_201_CREATED, tags=['Users'], response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['Users'])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['Users'])
def get_single_user(id, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found!'
        )
    return user.first()


@router.delete('/user/{id}', tags=['Users'])
def delete_user(id, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {id} not found'
        )
    user.delete(synchronize_session=False)
    db.commit()
    return f'User {id} deleted!'


@router.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Users'])
def update_user(id, request: schemas.User, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found!'
        )
    user.update(dict(request))
    db.commit()
    return f'User {id} updated!'
