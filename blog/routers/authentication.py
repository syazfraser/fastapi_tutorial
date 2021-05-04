from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, hashing
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: schemas.LogIn, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.name == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Credentials/User {request.username} not found'
        )
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Password!'
        )
    # Generate a JWT Token and return
    return user
