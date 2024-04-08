from pymongo import MongoClient

conn_string = "mongodb://localhost:27017/"

client = MongoClient()
sculture_db = client.sculture
users_collection = sculture_db.users
posts_collection = sculture_db.posts
feedback_collection = sculture_db.feedback