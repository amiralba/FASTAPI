from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first() be jaye in balayio mizarim chon toye oauth request form emailo neveshte username
    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail= f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail= f"Invalid Credentials")
    
    #create a token and return it

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}
    
