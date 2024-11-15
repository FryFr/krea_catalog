from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def connect_db():
    db.client = AsyncIOMotorClient(settings.mongodb_uri)
    db.database = db.client[settings.mongodb_db]

async def close_db():
    db.client.close()
