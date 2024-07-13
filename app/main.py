from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:    
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break #toye while break yadet bere be ga miri
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)



my_posts = [{"title": "title of post 1","content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "i like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}





@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) #status_code age nazarim code 200 mide behemon defualteshe vase hamin 201 besh midim ke vase create kardane
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published)) #order matters, # %s shabih ye place holdere ke vase inke sql injection nakhorim miaim ino mizrim va badesh joda vraible hamono midim besh
    new_post = cursor.fetchone()
    conn.commit()  #age ino nazarim toye api doros neshon mide ama post toye db save nemishe
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest_post": post}

# age in latest payin tare get id payini bashe, chon az bala mikhone miad payyin vaghti latest get mikoni miad toye
#path latesto mizare jaye {id} bad nmitone be int tabdil kone error mide pas tartib moheme kheeili

@app.get("/posts/{id}")
def get_post(id: int):  #hatman byd id: int bezarim ke id o be int tabdil kone ke def find_post doros kar kone
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
        #be jaye 2 khate payin on bala httpexception import mikonim va khate bala ro minevisim
        # response.status_code = status.HTTP_404_NOT_FOUND    
        # return {"message": f"post with id: {id} was not found"} 
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None: #ino mizarim ke age id besh bedim ke mojod nabashe betone ye javabi bede va error nade
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT) #vaghti 204 estefade mikoni hich returni behet nmide server vase hamin inja message benevisi neshon nemide pas miai respons mizari ke error nade


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return {"data": updated_post}
