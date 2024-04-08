from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
import pymongo
import hashlib
from datetime import datetime
from database.initialize import users_collection, posts_collection, feedback_collection


app = FastAPI()

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserAdd(UserBase):
    api_key: str
    active: bool=False

class PostBase(BaseModel):
    title: str
    body: str

class PostAdd(PostBase):
    created: datetime
    author_id: str
    active: bool = False
    thumbs_up: list
    thumbs_down: list



users_local_db = []
posts_local_db = []
feedback_local_db = []

def hashed_token(email, salt="1325143SomethingTotest21521"):
    password_hash = hashlib.sha256((email + salt).encode('utf-8')).hexdigest()
    return password_hash

@app.get('/')
async def root():
    return {"message": "hello world"}

def find_user_token(token: str):
    try: 
        return users_collection.find_one({'api_key': token})
    except:
        raise HTTPException(status_code = 403, detail="Unathorised, No user Found")
    
def create_user_db(user: UserAdd):
    try:
        user_id = users_collection.insert_one(dict(user)).inserted_id
    except:
        raise HTTPException(status_code = 500, detail="Problem with saving the data to database")
    return user_id

def get_user_db(id: str):
    return users_collection.find_one({"_id": id})

def create_post_db(post: PostAdd):
    try:
        return posts_collection.insert_one(dict(post)).inserted_id
    except:
        raise HTTPException(status_code = 500, detail="Problem with saving the data to database")
    
def get_post_db(id: str):
    result = posts_collection.find_one({"_id": ObjectId(id)})
    # print(result)
    return result

def update_thumbs_up(id: str, users_list: list):
    posts_collection.update_one({"_id": ObjectId(id)}, {"$set": {"thumbs_up":users_list}})

def update_thumbs_down(id: str, users_list: list):
    posts_collection.update_one({"_id": ObjectId(id)}, {"$set": {"thumbs_down":users_list}})

def get_last_posts_db():
    return posts_collection.find({"active": True})

@app.post('/users')
async def create_user(user_base: UserBase):
    api_key = hashed_token(user_base.email)
    add_user = UserAdd(first_name=user_base.first_name, last_name=user_base.last_name, email=user_base.email, api_key=api_key, active=True)

    user_id = create_user_db(add_user)
    user_inst = get_user_db(user_id)


    # users_local_db.append(user)
    return {"user_api_key": user_inst['api_key']}

@app.post("/posts")
async def create_post(token: str, post: PostBase):
    user = find_user_token(token)
    user_id = str(user['_id'])
    post_add = PostAdd(title = post.title, body = post.body, active = True, created = datetime.now(), author_id = user_id, thumbs_up = [], thumbs_down=[])
    post_id = str(create_post_db(post_add))

    return {"post_id": post_id}

@app.post("/posts/upvote")
async def upvote_post(token: str, post_id: str):
    user = find_user_token(token)
    # print(user)
    post_inst = get_post_db(post_id)
    # print(post_inst)
    current_list = post_inst['thumbs_up']
    current_list.append(str(user['_id']))
    print(current_list)
    update_thumbs_up(post_id, current_list)
    return {"message": current_list}


@app.post("/posts/downvote")
async def downvote_post(token: str, post_id: str):
    user = find_user_token(token)
    post_inst = get_post_db(post_id)
    # print(user)
    post_inst = get_post_db(post_id)
    # print(post_inst)
    current_list = post_inst['thumbs_down']
    current_list.append(str(user['_id']))
    print(current_list)
    update_thumbs_down(post_id, current_list)
    return {"message": current_list}


@app.get('/posts/last')
async def get_last_posts():
    last_posts = get_last_posts_db()
    # print(last_posts)
    posts_list = [str(post['_id']) for post in last_posts]
    # print(posts_list)
    return {"data": posts_list}
