
from sqlalchemy import TIMESTAMP, Column, String, Integer, Boolean,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)


class Projects(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer,primary_key=True,nullable=False)
    project_name = Column(String,nullable=False,unique=True)
    project_tag = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    update_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    description = Column(String,nullable=False)
