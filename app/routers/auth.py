from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import oauth2,schemas,models,util
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/",response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email_name == user_credential.username
    ).first()
    if user.id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if not util.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    access_token = oauth2.create_token({'user_id':user.id,"user_email":user.email_name})
    return {"access_token":access_token,"token_type":"bearer"}