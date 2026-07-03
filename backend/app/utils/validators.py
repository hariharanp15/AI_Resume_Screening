def normalize_skills(skills: list[str]) -> list[str]:
    return sorted({skill.strip() for skill in skills if skill and skill.strip()})
