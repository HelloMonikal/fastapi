from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas
from .. import models,util
from .. database import get_db
from typing import List


router = APIRouter(
    prefix='/users'
    ,tags=["User"]
)

@router.get('/{id}',response_model=schemas.UserOut)
def get_user_id(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user.first()

@router.get('/',response_model=List[schemas.UserOut])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserIn,db:Session = Depends(get_db)):
    user.password = util.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    

