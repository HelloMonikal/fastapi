from datetime import datetime,timedelta
from jose import JWSError, jwt
from . import schemas,models
from sqlalchemy.orm import Session
from .database import get_db
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get('user_id')
        email = payload.get('user_email')
        if id is None or email is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id,email=email)
    except JWSError:
        raise credential_exception
    return token_data


def get_current_user(token:str = Depends(oauth2_schema)
                     ,db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not valid credential'
                                         ,headers={"WWW-Authentication":"Bearer"})
    token_data = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user.id