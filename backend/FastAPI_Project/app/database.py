from pymongo import MongoClient
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Set your MongoDB URI (change this to your MongoDB URI)
MONGO_URI = "mongodb://mongo:gvIXvVistiZoXBdOeLXLcJaZLDoWMsFu@autorack.proxy.rlwy.net:32955"
DATABASE_NAME = "Krea"

# Connecting to the database
client = MongoClient(MONGO_URI)
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Function to convert ObjectId to string
def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# Middleware to serialize MongoDB results
def serialize_item(item):
    if item:
        item["_id"] = convert_objectid_to_str(item["_id"])
    return item

def serialize_list(items):
    return [serialize_item(item) for item in items]
