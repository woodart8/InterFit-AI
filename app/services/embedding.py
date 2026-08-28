import os

from openai import OpenAI

from app.schemas.resume import ResumeChunk, EmbeddedResumeChunk


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def embed_chunks(
    chunks: list[ResumeChunk],
) -> list[EmbeddedResumeChunk]:

    if not chunks:
        return []

    texts = [
        f"{chunk.title}\n{chunk.content}"
        for chunk in chunks
    ]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )

    return [
        EmbeddedResumeChunk(
            type=chunk.type,
            title=chunk.title,
            content=chunk.content,
            embedding=item.embedding,
        )
        for chunk, item in zip(chunks, response.data)
    ]