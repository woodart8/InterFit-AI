import os

from pymongo import MongoClient


MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://mongo:27017"
)

MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "interfit"
)

client = MongoClient(MONGODB_URL)

db = client[MONGODB_DATABASE]

resume_collection = db["resumes"]
resume_chunk_collection = db["resume_chunks"]