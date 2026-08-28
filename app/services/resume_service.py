from app.services.parser import extract_text_from_pdf
from app.services.llm import structure_resume
from app.services.chunker import create_resume_chunks
from app.services.embedding import embed_chunks
from app.repositories.resume_repository import (
    save_resume,
    save_resume_chunks,
)


def process_resume(
    file_data: bytes,
    filename: str,
):
    # PDF → Text
    text = extract_text_from_pdf(file_data)

    # Text → ResumeSchema
    resume = structure_resume(text)

    # ResumeSchema → ResumeChunk
    chunks = create_resume_chunks(resume)

    # ResumeChunk → EmbeddedResumeChunk
    embedded_chunks = embed_chunks(chunks)

    # Resume 저장
    resume_id = save_resume(
        filename=filename,
        resume=resume.model_dump(),
    )

    # Embedded Chunk 저장
    save_resume_chunks(
        resume_id=resume_id,
        chunks=embedded_chunks,
    )

    return {
        "resume_id": str(resume_id),
        "chunk_count": len(embedded_chunks),
    }