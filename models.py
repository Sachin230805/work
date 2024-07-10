from .database import Base
from sqlalchemy import Column,Integer,PrimaryKeyConstraint,Nullable,String

class Post(Base):
    __tablename__="posts"

    id=Column(Integer,PrimaryKeyConstraint=True,Nullable=False)
    name=Column(String,Nullable=False)
    company_name=Column(String,Nullable=False)
    age=Column(Integer,Nullable=False)    