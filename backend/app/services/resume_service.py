from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.config.settings import get_settings
from app.utils.docx_reader import read_docx_text
from app.utils.file_upload import save_upload
from app.utils.pdf_reader import read_pdf_text


async def save_and_extract_resume(file: UploadFile) -> tuple[Path, str]:
    destination = await save_upload(file, Path(get_settings().uploads_dir))
    if destination.suffix.lower() == ".pdf":
        text = read_pdf_text(destination)
    else:
        text = read_docx_text(destination)
    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract readable text from resume")
    return destination, text
