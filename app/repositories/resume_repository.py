from app.db.mongodb import db
from app.schemas.resume import EmbeddedResumeChunk
from bson import ObjectId

resume_collection = db["resumes"]
resume_chunk_collection = db["resume_chunks"]


def save_resume(
    filename: str,
    resume: dict,
):
    result = resume_collection.insert_one(
        {
            "filename": filename,
            "resume": resume,
        }
    )

    return result.inserted_id


def save_resume_chunks(
    resume_id,
    chunks: list[EmbeddedResumeChunk],
):
    if not chunks:
        return 0

    documents = [
        {
            "resume_id": resume_id,
            "type": chunk.type,
            "title": chunk.title,
            "content": chunk.content,
            "embedding": chunk.embedding,
        }
        for chunk in chunks
    ]

    result = resume_chunk_collection.insert_many(documents)

    return len(result.inserted_ids)


def find_resume(resume_id: str):
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return None

    return resume_collection.find_one({
        "_id": object_id
    })


def search_resume_chunks(
    resume_id: str,
    embedding: list[float],
    limit: int = 5,
):
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return []

    pipeline = [
        {
            "$vectorSearch": {
                "index": "resume_vector_index",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": limit * 10,
                "limit": limit,
                "filter": {
                    "resume_id": object_id,
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "type": 1,
                "title": 1,
                "content": 1,
                "score": {
                    "$meta": "vectorSearchScore",
                },
            }
        },
    ]

    return list(
        resume_chunk_collection.aggregate(pipeline)
    )


def get_resume_chunks(
    resume_id: str,
    limit: int = 10,
):
    try:
        object_id = ObjectId(resume_id)
    except Exception:
        return []

    return list(
        resume_chunk_collection.find(
            {
                "resume_id": object_id,
            },
            {
                "_id": 0,
                "type": 1,
                "title": 1,
                "content": 1,
            },
        ).limit(limit)
    )