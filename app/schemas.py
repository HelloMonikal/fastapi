from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint



class UserIn(BaseModel):
    email:EmailStr
    password :str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime


class PostBase(BaseModel):
    title:str
    content:str    
    created_at:datetime
    class config:
        orm_mode =True


class PostGet(PostBase):
    pass
    owner_id:int
    owner:UserOut


class Updated(PostBase):
    ...



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]
    email:EmailStr

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1) # type: ignore


class ProjectOut(BaseModel):
    project_name:str
    project_tag:str
    created_at:datetime
    update_at:datetime
    description:str
