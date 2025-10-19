from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from .. database import get_db
from ..oauth2 import get_current_user


router = APIRouter(
    prefix='/vote'
    ,tags=["Vote"]
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(get_db),current_user:int = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if post_query.first() is None: ##check if the post exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {vote.post_id} doesn't exit")
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user
                                              ,models.Vote.post_id == vote.post_id)
    
    found_vote = vote_query.first()
    if vote.dir == 1: #to like the post
        if found_vote:  #check if the user has liked the post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user} has already liked the post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else: # to unlike the post
        if not found_vote:  # check if the user has liked the post
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,detail="Vote doesn't exit")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully cancel the vote"}
        




