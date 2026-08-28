import pymupdf

def extract_text_from_pdf(file_data: bytes) -> str:
    """
    PDF 파일의 bytes를 받아 전체 텍스트를 추출한다.
    """

    document = pymupdf.open(
        stream=file_data,
        filetype="pdf"
    )

    try:
        text = "\n".join(
            page.get_text()
            for page in document
        )

        return text.strip()

    finally:
        document.close()