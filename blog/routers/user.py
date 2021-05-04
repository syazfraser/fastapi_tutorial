from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, database, hashing, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_single_user(id, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found!'
        )
    return user.first()


@router.delete('/{id}')
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


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
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
