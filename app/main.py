from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()



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




@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) #status_code age nazarim code 200 mide behemon defualteshe vase hamin 201 besh midim ke vase create kardane
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published)) #order matters, # %s shabih ye place holdere ke vase inke sql injection nakhorim miaim ino mizrim va badesh joda vraible hamono midim besh
    # new_post = cursor.fetchone()
    # conn.commit()  #age ino nazarim toye api doros neshon mide ama post toye db save nemishe

    # new_post = models.Post(title=post.title, content=post.content, published=post.published) kheili tolanie az raveshe zir estefade mikonim
   
    new_post = models.Post(**post.model_dump()) #**post.model_dump() unpack mikone tile va content va baghie chizaro niaz nis tak tak benevisim age badanam ezafe konim khodesh ok mikone
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest_post": post}

# age in latest payin tare get id payini bashe, chon az bala mikhone miad payyin vaghti latest get mikoni miad toye
#path latesto mizare jaye {id} bad nmitone be int tabdil kone error mide pas tartib moheme kheeili

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):  #hatman byd id: int bezarim ke id o be int tabdil kone ke def find_post doros kar kone
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # print(post)

    post = db.query(models.Post).filter(models.Post.id == id).first() #age .all() bzrim hata age peyda kone bzm donbalesh migarde ama id fght 1 done drim pas first mizrim ke be avalin id moshabeh resid dg nagarde
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
        #be jaye 2 khate payin on bala httpexception import mikonim va khate bala ro minevisim
        # response.status_code = status.HTTP_404_NOT_FOUND    
        # return {"message": f"post with id: {id} was not found"} 
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None: #ino mizarim ke age id besh bedim ke mojod nabashe betone ye javabi bede va error nade
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
