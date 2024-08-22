from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from . import models
from .database import engine
from .routers import user, post, auth, vote


sentry_sdk.init(
    dsn="https://fe4c94de246c6f5d64382becdd482d86@o4507786394009600.ingest.de.sentry.io/4507786397352016",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

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
    return {"message": "Hello world! This is my first project ever"}

