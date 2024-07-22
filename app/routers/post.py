from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",   #be jaye inke too hame /post benevisim inja fixesh mikonim age +{id} bashe "/{id}" kafie
    tags=['Posts']   #toye /docs, daste bandi mikone
)




@router.get("/")
def get_posts(db: Session = Depends(get_db), response_model=schemas.Post):
    
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #status_code age nazarim code 200 mide behemon defualteshe vase hamin 201 besh midim ke vase create kardane
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(**post.model_dump()) #**post.model_dump() unpack mikone tile va content va baghie chizaro niaz nis tak tak benevisim age badanam ezafe konim khodesh ok mikone
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=schemas.Post):  #hatman byd id: int bezarim ke id o be int tabdil kone ke def find_post doros kar kone


    post = db.query(models.Post).filter(models.Post.id == id).first() #age .all() bzrim hata age peyda kone bzm donbalesh migarde ama id fght 1 done drim pas first mizrim ke be avalin id moshabeh resid dg nagarde
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
 
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None: #ino mizarim ke age id besh bedim ke mojod nabashe betone ye javabi bede va error nade
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):


    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()