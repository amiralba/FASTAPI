from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, post, auth, vote


#payini dg kar nmikone chon alembic kar mikone be jash
# models.Base.metadata.create_all(bind=engine)

origins= ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   #inja mitonim moshakhas konim che http requesti mitonan befresan msln age bezarim get fght mitonn get befresan
    allow_headers=["*"],  
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!!!!"}