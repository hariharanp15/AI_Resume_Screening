def build_interview_invitation(to_email: str, candidate_name: str, job_title: str) -> dict:
    return {
        "to": to_email,
        "subject": f"Interview invitation for {job_title}",
        "body": f"Hello {candidate_name}, we would like to invite you to interview for {job_title}.",
    }
