from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class User(BaseModel):
    first_name: str
    last_name: str
    active: bool = False
    api_key: str

class PostBase(BaseModel):
    title: str
    body: str
    active: bool = False

class PostAdd(PostBase):
    created: str
    author_id: str


users_local_db = []
posts_local_db = []
feedback_local_db = []

@app.get('/')
async def root():
    return {"message": "hello world"}


@app.post('/users')
async def create_user(user: User):
    users_local_db.append(user)
    return {"users": users_local_db}

@app.post("/posts")
async def create_post(token: str, post: PostBase):
    for user in users_local_db:
        print(user.api_key)
        print(token)
        if user.api_key == token:
            posts_local_db.append(post)
        else:
            raise HTTPException(status_code = 403, detail="Unauthorised")
    return {"posts": posts_local_db}

