import re
from pathlib import Path
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from docx import Document
from .embeddings import local_embedding


SKILL_BANK = {
    "python", "fastapi", "django", "flask", "react", "typescript", "javascript", "sql",
    "postgresql", "mysql", "docker", "kubernetes", "aws", "azure", "gcp", "git",
    "machine learning", "nlp", "pandas", "numpy", "tensorflow", "pytorch", "java",
    "spring", "node", "express", "mongodb", "redis", "ci/cd", "leadership", "agile",
}


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_docx_text(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


async def save_and_parse_resume(file: UploadFile, upload_dir: Path) -> tuple[str, str]:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported")
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / f"{Path(file.filename or 'resume').stem}-{abs(hash(file.filename))}{extension}"
    destination.write_bytes(await file.read())
    text = extract_pdf_text(destination) if extension == ".pdf" else extract_docx_text(destination)
    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract readable text from resume")
    return str(destination), text


def extract_profile(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_match = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text)
    lowered = text.lower()
    skills = sorted(skill for skill in SKILL_BANK if skill in lowered)
    name = lines[0][:120] if lines else "Unknown Candidate"
    experience = "\n".join(line for line in lines if re.search(r"experience|engineer|developer|manager|analyst", line, re.I))[:1200]
    education = "\n".join(line for line in lines if re.search(r"degree|university|college|bachelor|master|phd|education", line, re.I))[:1200]
    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "skills": skills,
        "work_experience": experience or None,
        "education": education or None,
        "resume_text": text,
        "embedding": local_embedding(text),
    }
