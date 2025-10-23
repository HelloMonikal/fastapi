
from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import oauth2
from .. import schemas
from .. import models
from .. database import get_db


router = APIRouter(
    prefix='/posts'
    ,tags=["Post"]
)
# use id to get post by id 
@router.get('/{id}',response_model=schemas.PostOut)
def get_post_id(id:int,db:Session=Depends(get_db)
                 ,current_user:int=Depends(oauth2.get_current_user)
                 ,limit:int = 10):
    
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")
                    ).filter(models.Post.id==id).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).limit(limit).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return post

# get all posts
@router.get('/',response_model=List[schemas.PostOut])
def get_post(db:Session = Depends(get_db)
             ,current_user:int=Depends(oauth2.get_current_user)
             ,limit:int = 10
             ,search:Optional[str] = ""
             ):
    # posts = db.query(models.Post).limit(limit=limit).all()

    # result = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).all()


    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                      ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

    return result
    

 
#to create post
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(new_post:schemas.PostBase,db:Session = Depends(get_db)
                ,current_user:int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user,**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#to update post by id
@router.put('/{id}',response_model=schemas.Post)
def update_post(id:int,new_post:schemas.PostBase,db:Session=Depends(get_db)
                 ,current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='No credential to update')
    post_query.update(new_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()


# to delete post by id
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)
                 ,current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='No credential to delete')
    post_query.delete(synchronize_session=False)
    db.commit()