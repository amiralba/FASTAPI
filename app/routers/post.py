from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",   #be jaye inke too hame /post benevisim inja fixesh mikonim age +{id} bashe "/{id}" kafie
    tags=['Posts']   #toye /docs, daste bandi mikone
)


#limit va skip toye api call miznim, {{URL}}posts?limit=2&skip=2&search=hello%20world
#vase search &search ham ezafe mishe be balayi,,, %20 yani space
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#age bekhaym postaye khode useri ke sign krde ro fght neshone khodesh bede az ghesmate bala ino taghir midim:
# posts = db.query(models.Post).filter(models.POst.owner_id == current_user.id).all()





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #status_code age nazarim code 200 mide behemon defualteshe vase hamin 201 besh midim ke vase create kardane
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) #**post.model_dump() unpack mikone tile va content va baghie chizaro niaz nis tak tak benevisim age badanam ezafe konim khodesh ok mikone
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  #hatman byd id: int bezarim ke id o be int tabdil kone ke def find_post doros kar kone


    post = db.query(models.Post).filter(models.Post.id == id).first() #age .all() bzrim hata age peyda kone bzm donbalesh migarde ama id fght 1 done drim pas first mizrim ke be avalin id moshabeh resid dg nagarde
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None: #ino mizarim ke age id besh bedim ke mojod nabashe betone ye javabi bede va error nade
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()