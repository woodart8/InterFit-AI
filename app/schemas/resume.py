from pydantic import BaseModel, Field


class BasicInfo(BaseModel):
    name: str = Field(
        default="",
        description="이력서에 명시된 이름"
    )
    position: str = Field(
        default="",
        description="지원 직무 또는 희망 직무. 이력서의 지원분야, 지원직무 등에서 명시된 값을 사용"
    )
    introduction: str = Field(
        default="",
        description="자기소개서, 자기소개, 본인소개 등에서 작성된 자기소개 내용"
    )


class Skills(BaseModel):
    language: list[str] = Field(
        default_factory=list,
        description="실제로 사용하거나 학습했다고 명시된 프로그래밍 언어 및 SQL"
    )
    framework: list[str] = Field(
        default_factory=list,
        description="실제로 사용했다고 명시된 프레임워크 및 라이브러리"
    )
    database: list[str] = Field(
        default_factory=list,
        description="실제로 사용했다고 명시된 데이터베이스 및 저장소"
    )
    infrastructure: list[str] = Field(
        default_factory=list,
        description="실제로 사용했다고 명시된 인프라, 메시지 브로커, 클라우드 등의 기술"
    )
    tool: list[str] = Field(
        default_factory=list,
        description="실제로 사용했다고 명시된 개발 및 테스트 도구"
    )
    etc: list[str] = Field(
        default_factory=list,
        description="위 분류에 포함되지 않는 실제 사용 기술"
    )


class Experience(BaseModel):
    company: str = Field(
        default="",
        description="회사 또는 조직명"
    )
    role: str = Field(
        default="",
        description="해당 경험에서의 직무 또는 역할"
    )
    period: str = Field(
        default="",
        description="경험 기간"
    )
    responsibilities: list[str] = Field(
        default_factory=list,
        description="실제로 수행한 업무"
    )
    achievements: list[str] = Field(
        default_factory=list,
        description="원문에 명시된 객관적인 성과만 기록. 추측 금지"
    )


class Project(BaseModel):
    name: str = Field(
        default="",
        description=(
            "이력서 전체에서 확인되는 프로젝트명. "
            "프로젝트 항목뿐 아니라 자기소개서나 역량기술서에서 "
            "프로젝트명 또는 시스템/서비스명이 언급된 경우도 포함"
        )
    )
    period: str = Field(
        default="",
        description="프로젝트 기간. 명시되지 않은 경우 빈 문자열"
    )
    description: str = Field(
        default="",
        description="프로젝트의 목적과 내용을 원문에 근거하여 요약"
    )
    role: str = Field(
        default="",
        description="프로젝트에서 맡은 역할. 명시되지 않은 경우 빈 문자열"
    )
    technologies: list[str] = Field(
        default_factory=list,
        description=(
            "해당 프로젝트에서 실제 사용했다고 명시된 기술. "
            "프로젝트와 관련 없이 단순 언급된 기술은 포함하지 않음"
        )
    )
    problem: str = Field(
        default="",
        description="프로젝트에서 실제로 언급된 문제, 배경 또는 해결해야 했던 과제"
    )
    solution: str = Field(
        default="",
        description="문제를 해결하기 위해 실제로 수행한 방법"
    )
    result: str = Field(
        default="",
        description=(
            "원문에 명시된 결과 또는 객관적인 성과. "
            "원문에 결과가 없다면 빈 문자열. "
            "성능 향상이나 사용자 경험 개선 등을 임의로 추론하지 않음"
        )
    )
    responsibilities: list[str] = Field(
        default_factory=list,
        description="프로젝트에서 실제로 수행한 업무"
    )


class Education(BaseModel):
    school: str = Field(
        default="",
        description="학교명"
    )
    major: str = Field(
        default="",
        description="전공"
    )
    degree: str = Field(
        default="",
        description="학위 또는 졸업 상태"
    )
    period: str = Field(
        default="",
        description="재학 기간"
    )
    gpa: str = Field(
        default="",
        description="학점. 원문에 명시된 형식을 최대한 유지"
    )


class Certification(BaseModel):
    name: str = Field(
        default="",
        description="자격증명"
    )
    issuer: str = Field(
        default="",
        description="발급기관"
    )
    date: str = Field(
        default="",
        description="취득일"
    )


class Award(BaseModel):
    name: str = Field(
        default="",
        description="수상명"
    )
    organization: str = Field(
        default="",
        description="수상 기관 또는 주최기관"
    )
    date: str = Field(
        default="",
        description="수상일"
    )


class ResumeSchema(BaseModel):
    basic_info: BasicInfo
    skills: Skills
    experiences: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    awards: list[Award] = Field(default_factory=list)

class ResumeChunk(BaseModel):
    type: str
    title: str
    content: str

class EmbeddedResumeChunk(BaseModel):
    type: str
    title: str
    content: str
    embedding: list[float]