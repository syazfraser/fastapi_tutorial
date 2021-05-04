from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import status, HTTPException


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found!'
        )
    return user.first()


def delete(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with {id} not found'
        )
    user.delete(synchronize_session=False)
    db.commit()
    return f'User {id} deleted!'


def update(id, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found!'
        )
    user.update(dict(request))
    db.commit()
    return f'User {id} updated!'
