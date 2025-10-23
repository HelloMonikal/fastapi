from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import oauth2,schemas,models,util
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/",response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credential.username
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invaild Credentials')
    if not util.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invaild Credentials')
    
    access_token = oauth2.create_token({'user_id':user.id,"user_email":user.email})
    
    return {"access_token":access_token,"token_type":"bearer"}