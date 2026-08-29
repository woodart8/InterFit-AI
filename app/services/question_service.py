import os
from uuid import uuid4

from openai import OpenAI

from app.schemas.interview import InterviewQuestion
from app.services.rag_service import search_relevant_resume_chunks


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_next_question(
    resume_id: str,
    previous_question: str,
    answer: str,
) -> InterviewQuestion:

    # 1. 답변 기반으로 이력서 관련 정보 검색
    relevant_chunks = search_relevant_resume_chunks(
        resume_id=resume_id,
        answer=answer,
        limit=5,
    )

    # 2. RAG 결과를 LLM에 전달할 문자열로 변환
    resume_context = "\n\n".join(
        [
            f"""
제목: {chunk["title"]}
내용:
{chunk["content"]}
""".strip()
            for chunk in relevant_chunks
        ]
    )

    # 검색 결과가 없는 경우
    if not resume_context:
        resume_context = "관련된 이력서 정보를 찾지 못했습니다."

    # 3. LLM으로 다음 질문 생성
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
당신은 백엔드 개발자 채용 면접관입니다.

지원자의 이전 질문과 답변,
그리고 지원자의 이력서에서 검색된 관련 정보를 바탕으로
다음 면접 질문을 하나 생성하세요.

규칙:
- 지원자의 답변과 관련된 질문을 생성하세요.
- 이력서에 실제로 존재하는 내용을 활용하세요.
- 지원자가 언급한 기술이나 프로젝트에 대해 구체적으로 질문하세요.
- 답변에 대한 꼬리질문을 우선적으로 고려하세요.
- 단순한 반복 질문은 하지 마세요.
- 실제 기술 면접에서 사용할 수 있는 질문을 생성하세요.
- 질문 하나만 출력하세요.
- 질문 앞에 번호나 설명을 붙이지 마세요.
""",
            },
            {
                "role": "user",
                "content": f"""
[이전 질문]
{previous_question}

[지원자의 답변]
{answer}

[지원자의 이력서 관련 정보]
{resume_context}

위 정보를 바탕으로 다음 면접 질문을 하나 생성하세요.
""",
            },
        ],
        temperature=0.7,
    )

    question_content = response.choices[0].message.content.strip()

    return InterviewQuestion(
        id=uuid4().hex,
        content=question_content,
    )