from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime

 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

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


#reponse

class Post(PostBase):  #toye khode PostBase 3 ta iteme title content va published hast niaz nis dobre benevisim
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  #classe userout bayad balatare in khat bashe ke error nade. 

    model_config = {
        'from_attributes': True
    }




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
    


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]
    
