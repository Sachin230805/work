from fastapi import FastAPI,Body,status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import time
 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
class User(BaseModel):
    name: str
    age: int
    company_name: str = None
    id:int

try:
     conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Sachin@123',cursor_factory=RealDictCursor)
     cursor=conn.cursor()
     print("connection was successful")
except Exception as error:
     print("connection was unsuccessful")

users=[{"name":"SACHIN","age":18,"company_name":"SEEDFLEX","id":10},{"name":"WADZEE","age":23,"company_name":"SEEDFLEX","id":12},
      {"name":"ADITYA","age":36,"company_name":"SEEDFLEX","id":13},{"name":"ADAM","age":28,"company_name":"SEEDFLEX","id":14},
      {"name":"GEORGE","age":37,"company_name":"SEEDFLEX","id":15},{"name":"MUSTAFA","age":53,"company_name":"SEEDFLEX","id":16}]


def return_posts(id:int):
    for i in users:                
        if i["id"]==id:
            return i
    return None

def del_post(id:int):
    for i,p in enumerate(users):
        if p["id"]==id:
            return i
    return None          

@app.get("/")
def main_page():
    return("WELCOME TO SEEDFLEX")

@app.post("/posts")
def creat_posts(new_post: User):
        newpost=new_post.dict()
        users.append(newpost)
        return(newpost)
        
@app.get("/post")
def create_posts():
    return users

@app.get("/posts/latest")
def latest_post():
    if users:
        return users[-1]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/posts/{id}")
def get_post(id:int):
    index=return_posts(id)
    if index:
      return(index)
    else:
        return("User not found")
      
@app.delete("/post/delete/{id}")
def delete_post(id:int):
    index1=del_post(id)
    if index1 is not None:
     users.pop(index1)
     return(f"the ID {id} was removed")
    else:
        return(f"{id} not found")
    
@app.get("/poststable")
def get_table():
    cursor.execute("""select * from social""")
    table=cursor.fetchall()
    return(table)

@app.post("/posts/createposts")
def createe_posts(post:User):
    cursor.execute("""insert into social (id,name,company_name,age) values (%s,%s,%s,%s) returning *""" ,
                   (post.id,post.name,post.company_name,post.age))
    new_post=cursor.fetchone()
    conn.commit()
    
    return new_post

@app.get("/posts/tablepost/{id}")
def get_tablepost(id:str):
    cursor.execute("""select from social where id= %s""",(str(id),))
    tablepost=cursor.fetchone()
    
    if not tablepost:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return tablepost

