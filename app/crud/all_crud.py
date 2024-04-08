import hashlib
from fastapi import HTTPException
from database.initialize import users_collection, posts_collection
from bson.objectid import ObjectId
from schemas.all_schema import UserAdd, UserBase, PostAdd, PostBase
import pymongo




def find_user_token(token: str):
    try: 
        output = users_collection.find_one({'api_key': token})
        if output == None:
            raise HTTPException(status_code = 403, detail="Unathorised, No user Found")
        else:
            return output
                                           
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
    return posts_collection.find({"active": True}, limit=10).sort('created',pymongo.DESCENDING)