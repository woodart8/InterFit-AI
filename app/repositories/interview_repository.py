from datetime import datetime, timezone

from bson import ObjectId

from app.db.mongodb import db


interview_collection = db["interviews"]


def create_interview(
    interview_id: str,
    resume_id: str,
    question_id: str,
    question: str,
):
    document = {
        "_id": interview_id,
        "resume_id": ObjectId(resume_id),
        "questions": [
            {
                "question_id": question_id,
                "content": question,
                "answer": None,
            }
        ],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    interview_collection.insert_one(document)

    return interview_id


def find_interview(interview_id: str):
    return interview_collection.find_one({
        "_id": interview_id
    })


def save_question(
    interview_id: str,
    question_id: str,
    question: str,
):
    result = interview_collection.update_one(
        {
            "_id": interview_id,
        },
        {
            "$push": {
                "questions": {
                    "question_id": question_id,
                    "content": question,
                    "answer": None,
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc),
            },
        },
    )

    return result.modified_count > 0


def save_answer(
    interview_id: str,
    question_id: str,
    answer: str,
):
    result = interview_collection.update_one(
        {
            "_id": interview_id,
            "questions.question_id": question_id,
        },
        {
            "$set": {
                "questions.$.answer": answer,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    return result.modified_count > 0