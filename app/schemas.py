from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#reponse

class Post(PostBase):  #toye khode PostBase 3 ta iteme title content va published hast niaz nis dobre benevisim
    id: int
    created_at: datetime

    model_config = {
        'from_attributes': True
    }




#users

class UserCreate(BaseModel):
    email: EmailStr  #Emailstr emailo formatesho tayid mikone
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {     #orm_mode toye version jadid injori neveshte mishe
        'from_attributes': True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    




