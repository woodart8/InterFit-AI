from app.db.mongodb import db
from app.schemas.resume import EmbeddedResumeChunk


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