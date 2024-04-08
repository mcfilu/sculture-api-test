from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
import pymongo
import hashlib
from datetime import datetime
from database.initialize import users_collection, posts_collection, feedback_collection
from helpers import hashed_token
from crud.all_crud import get_last_posts_db, get_post_db, get_user_db, create_user_db, create_post_db, update_thumbs_down, update_thumbs_up, find_user_token
from schemas.all_schema import UserAdd, UserBase, PostAdd, PostBase


app = FastAPI()


users_local_db = []
posts_local_db = []
feedback_local_db = []

@app.get('/')
async def root():
    """
    Welcome to page endpoint
    """
    return {"message": "hello world"}



@app.post('/users')
async def create_user(user_base: UserBase):
    """
    Create User Endpoint
    Requirs user base class information
    Return hashed api_key secret
    """
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


@app.get("/posts/last/detailed")
async def get_last_detailed_posts():
    detailed_list = []
    last_posts = get_last_posts_db()
    # print(last_posts)
    posts_list = [str(post['_id']) for post in last_posts]
    for post_id in posts_list:
        post_inst = get_post_db(post_id)
        upvotes_len = len(post_inst['thumbs_up'])
        downvotes_len = len(post_inst['thumbs_down'])
        post_dict = {"id": post_id, "upvotes": upvotes_len, 'downvotes': downvotes_len}
        detailed_list.append(post_dict)
    # print(posts_list)
    return {"data": detailed_list}
