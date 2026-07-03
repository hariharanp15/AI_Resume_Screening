from app.models.candidate import Candidate
from app.models.job import JobDescription


def _answer_from_resume(candidate: Candidate, skill: str) -> str:
    experience = candidate.work_experience or candidate.resume_text[:260].strip()
    if experience:
        return f"Use examples from the resume that mention {skill}, then connect them to the project or responsibility described: {experience[:220]}"
    return f"The resume has limited detail for {skill}; ask the candidate to explain a real project, their role, and the result."


def generate_interview_questions(candidate: Candidate, job: JobDescription) -> dict:
    skills = candidate.skills[:5] or job.required_skills[:5] or ["the required technology stack"]
    lead_skill = skills[0]
    missing_skills = [skill for skill in job.required_skills if skill.lower() not in {item.lower() for item in candidate.skills}]
    strengths = candidate.skills[:3] or ["problem solving"]
    weakness = missing_skills[0] if missing_skills else "depth in the most business-critical requirement"
    return {
        "technical": [
            {
                "question": f"How have you used {skill} in a production project?",
                "answer": _answer_from_resume(candidate, skill),
            }
            for skill in skills[:3]
        ] + [{
            "question": f"Explain how you would debug a performance issue in a {lead_skill} service.",
            "answer": f"Look for a structured answer covering metrics, logs, bottleneck isolation, and a fix related to {lead_skill}.",
        }],
        "scenario_based": [
            {
                "question": f"You inherit a delayed {job.title} project. How would you prioritize delivery and quality?",
                "answer": "A strong answer should mention clarifying scope, ranking risks, protecting must-have requirements, and communicating trade-offs.",
            },
            {
                "question": f"The resume is strong in {strengths[0]} but weaker in {weakness}. How would you close that gap on this job?",
                "answer": f"The answer should acknowledge the gap in {weakness}, propose a learning or delivery plan, and connect existing strengths to the role.",
            },
            {
                "question": f"A stakeholder asks for a feature outside the {job.title} scope. How would you respond?",
                "answer": "Look for stakeholder empathy, impact assessment, documented trade-offs, and a clear escalation path.",
            },
        ],
        "behavioral": [
            {
                "question": "Tell me about a time you handled ambiguous requirements.",
                "answer": "The answer should include the situation, how requirements were clarified, what action was taken, and the outcome.",
            },
            {
                "question": "Describe a conflict with a teammate and how you resolved it.",
                "answer": "Listen for accountability, respectful communication, and a resolution that improved delivery or trust.",
            },
            {
                "question": f"What strength from your resume makes you suitable for this {job.title} role?",
                "answer": f"A resume-based answer should highlight {', '.join(strengths)} and tie it directly to the job responsibilities.",
            },
        ],
    }
