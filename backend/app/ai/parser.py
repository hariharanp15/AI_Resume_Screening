import re
from app.ai.embeddings import local_embedding
from app.utils.constants import DEFAULT_SKILL_BANK


def extract_resume_profile(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_match = re.search(r"(\+?\d[\d\s().-]{8,}\d)", text)
    lowered = text.lower()
    skills = sorted(skill for skill in DEFAULT_SKILL_BANK if skill in lowered)
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
