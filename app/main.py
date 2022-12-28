from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# # This will create tables (if they don't exist) in models.py every time the script starts up
# # Don't need this if you are using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# List of servers that can communicate with our API (ex : https://www.google.com)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}




