from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.utils.constants import SUPPORTED_RESUME_EXTENSIONS


async def save_upload(file: UploadFile, upload_dir: Path) -> Path:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in SUPPORTED_RESUME_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported")
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_stem = "".join(char for char in Path(file.filename or "resume").stem if char.isalnum() or char in {"-", "_"}).strip()
    destination = upload_dir / f"{safe_stem or 'resume'}-{abs(hash(file.filename))}{extension}"
    destination.write_bytes(await file.read())
    return destination
