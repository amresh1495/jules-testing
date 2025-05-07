import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017") # Default if not set
DATABASE_NAME = "spaced_repetition"

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client, db
    print(f"Attempting to connect to MongoDB at {MONGO_DETAILS}...")
    client = AsyncIOMotorClient(MONGO_DETAILS)
    db = client[DATABASE_NAME]
    try:
        # Check connection
        await client.admin.command('ping')
        print(f"Successfully connected to MongoDB database '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # Optionally re-raise or handle the error appropriately
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

def get_database():
    if db is None:
        # This case should ideally not happen if connect_to_mongo is called at startup
        # But as a fallback, could try connecting here, though it's better to manage lifespan explicitly
        raise Exception("Database not initialized. Call connect_to_mongo first.")
    return db
