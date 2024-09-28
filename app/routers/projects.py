from operator import or_
from fastapi import  Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from .. database import get_db
from typing import List, Optional


router = APIRouter(
    prefix='/projects'
    ,tags=["Project"]
)

@router.get('/',response_model=List[schemas.ProjectOut])
def get_post(db:Session = Depends(get_db)
             ,search:Optional[str]=""
             ,limit:int = 20):
    projects = db.query(models.Projects).filter(
        or_(
        models.Projects.project_name.contains(search),
        models.Projects.project_tag.contains(search))).limit(limit=limit).all()

    return projects

