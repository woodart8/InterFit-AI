from app.services.embedding import embed_chunks
from app.schemas.resume import ResumeChunk

from app.repositories.resume_repository import search_resume_chunks


def search_relevant_resume_chunks(
    resume_id: str,
    answer: str,
    limit: int = 5,
):
    # 답변을 embedding하기 위해 임시 ResumeChunk 생성
    chunk = ResumeChunk(
        type="answer",
        title="면접 답변",
        content=answer,
    )

    # 기존 embedding 함수를 재사용
    embedded = embed_chunks([chunk])

    if not embedded:
        return []

    embedding = embedded[0].embedding

    # 해당 이력서에서 유사한 chunk 검색
    return search_resume_chunks(
        resume_id=resume_id,
        embedding=embedding,
        limit=limit,
    )