from app.schemas.resume import ResumeChunk, ResumeSchema


def create_resume_chunks(resume: ResumeSchema) -> list[ResumeChunk]:
    chunks: list[ResumeChunk] = []

    # 기본 정보
    if resume.basic_info.introduction:
        chunks.append(
            ResumeChunk(
                type="basic_info",
                title="자기소개",
                content=resume.basic_info.introduction,
            )
        )

    # 기술 스택
    skill_groups = {
        "언어": resume.skills.language,
        "프레임워크": resume.skills.framework,
        "데이터베이스": resume.skills.database,
        "인프라": resume.skills.infrastructure,
        "도구": resume.skills.tool,
        "기타": resume.skills.etc,
    }

    skill_content = [
        f"{category}: {', '.join(values)}"
        for category, values in skill_groups.items()
        if values
    ]

    if skill_content:
        chunks.append(
            ResumeChunk(
                type="skills",
                title="기술 스택",
                content="\n".join(skill_content),
            )
        )

    # 경력
    for experience in resume.experiences:
        content = "\n".join(
            [
                f"회사: {experience.company}",
                f"역할: {experience.role}",
                f"기간: {experience.period}",
                f"담당 업무: {', '.join(experience.responsibilities)}",
                f"성과: {', '.join(experience.achievements)}",
            ]
        )

        chunks.append(
            ResumeChunk(
                type="experience",
                title=experience.company,
                content=content,
            )
        )

    # 프로젝트
    for project in resume.projects:
        content = "\n".join(
            [
                f"프로젝트: {project.name}",
                f"기간: {project.period}",
                f"설명: {project.description}",
                f"역할: {project.role}",
                f"기술: {', '.join(project.technologies)}",
                f"문제: {project.problem}",
                f"해결: {project.solution}",
                f"결과: {project.result}",
                f"담당 업무: {', '.join(project.responsibilities)}",
            ]
        )

        chunks.append(
            ResumeChunk(
                type="project",
                title=project.name,
                content=content,
            )
        )

    # 학력
    for education in resume.education:
        content = "\n".join(
            [
                f"학교: {education.school}",
                f"전공: {education.major}",
                f"학위: {education.degree}",
                f"기간: {education.period}",
                f"학점: {education.gpa}",
            ]
        )

        chunks.append(
            ResumeChunk(
                type="education",
                title=education.school,
                content=content,
            )
        )

    # 자격증
    for certification in resume.certifications:
        content = "\n".join(
            [
                f"자격증: {certification.name}",
                f"발급기관: {certification.issuer}",
                f"취득일: {certification.date}",
            ]
        )

        chunks.append(
            ResumeChunk(
                type="certification",
                title=certification.name,
                content=content,
            )
        )

    # 수상
    for award in resume.awards:
        content = "\n".join(
            [
                f"수상명: {award.name}",
                f"기관: {award.organization}",
                f"수상일: {award.date}",
            ]
        )

        chunks.append(
            ResumeChunk(
                type="award",
                title=award.name,
                content=content,
            )
        )

    return chunks