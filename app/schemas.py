from pydantic import BaseModel
 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass









#balayia rahat tare
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool
    #masalan mikhaim user faghat betone published edit kone inja fght published mizarim bashe baghie ro pak mikonim.


