from uuid import uuid4

from fastapi import HTTPException

from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewQuestion,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
)

from app.repositories.resume_repository import find_resume

from app.repositories.interview_repository import (
    create_interview,
    find_interview,
    save_answer,
    save_question,
)

from app.services.question_service import generate_next_question


def start_interview(
    request: InterviewStartRequest,
) -> InterviewStartResponse:

    resume = find_resume(request.resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="이력서를 찾을 수 없습니다.",
        )

    interview_id = uuid4().hex
    question_id = uuid4().hex

    question_content = "안녕하세요. 간단하게 자기소개 부탁드립니다."

    question = InterviewQuestion(
        id=question_id,
        content=question_content,
    )

    create_interview(
        interview_id=interview_id,
        resume_id=request.resume_id,
        question_id=question_id,
        question=question_content,
    )

    return InterviewStartResponse(
        interview_id=interview_id,
        question=question,
    )


def submit_answer(
    interview_id: str,
    request: InterviewAnswerRequest,
) -> InterviewAnswerResponse:

    # 1. 면접 조회
    interview = find_interview(interview_id)

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="면접을 찾을 수 없습니다.",
        )

    # 2. 현재 질문 찾기
    current_question = next(
        (
            question
            for question in interview["questions"]
            if question["question_id"] == request.question_id
        ),
        None,
    )

    if not current_question:
        raise HTTPException(
            status_code=404,
            detail="질문을 찾을 수 없습니다.",
        )

    # 3. 답변 저장
    saved = save_answer(
        interview_id=interview_id,
        question_id=request.question_id,
        answer=request.answer,
    )

    if not saved:
        raise HTTPException(
            status_code=500,
            detail="답변 저장에 실패했습니다.",
        )

    # 4. 다음 질문 생성
    next_question = generate_next_question(
        resume_id=interview["resume_id"],
        previous_question=current_question["content"],
        answer=request.answer,
    )

    # 5. 다음 질문 저장
    saved = save_question(
        interview_id=interview_id,
        question_id=next_question.id,
        question=next_question.content,
    )

    if not saved:
        raise HTTPException(
            status_code=500,
            detail="다음 질문 저장에 실패했습니다.",
        )

    # 6. 다음 질문 반환
    return InterviewAnswerResponse(
        interview_id=interview_id,
        question_id=request.question_id,
        answer=request.answer,
        next_question=next_question,
    )