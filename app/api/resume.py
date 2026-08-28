from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_service import process_resume


router = APIRouter()


@router.post("")
async def upload_resume(file: UploadFile = File(...)):
    file_data = await file.read()

    if not file_data.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="유효한 PDF 파일이 아닙니다.",
        )

    result = process_resume(
        file_data=file_data,
        filename=file.filename,
    )

    return {
        "filename": file.filename,
        **result,
    }