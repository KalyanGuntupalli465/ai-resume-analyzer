def get_resume_analysis_prompt(resume_text: str, ats_score: float, matched_skills: list, missing_skills: list, job_description: str = "") -> str:
    """
     prompt for resume analysis.
    """

    jd_section = f"""
    Job Description Provided:
{job_description}
""" if job_description.strip() else "No job description provided. Give general improvements."

    matched_str = ", ".join(matched_skills[:10]) if matched_skills else "None detected"
    missing_str = ", ".join(missing_skills[:10]) if missing_skills else "None"


    prompt = f"""
You are an expert resume reviewer and ATS optimization specialist with 10+ years of experience in tech recruiting.

Analyze the following resume and provide detailed, actionable feedback.

---

RESUME TEXT:
{resume_text[:3000]}

---

ATS SCORE: {ats_score}/100

MATCHED SKILLS FOUND: {matched_str}
MISSING IMPORTANT SKILLS: {missing_str}

{jd_section}

---

Please provide your analysis in the following exact JSON format and nothing else:

{{
    "overall_feedback": "2-3 sentence overall assessment of the resume",
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "improvements": [
        "specific improvement 1",
        "specific improvement 2",
        "specific improvement 3",
        "specific improvement 4"
    ],
    "missing_keywords": [
        "keyword 1",
        "keyword 2",
        "keyword 3"
    ],
    "rewrite_suggestions": [
        {{
            "original": "example weak bullet point from resume",
            "improved": "stronger rewritten version with metrics and action verbs"
        }}
    ],
    "ats_tips": [
        "ATS tip 1",
        "ATS tip 2",
        "ATS tip 3"
    ],
    "score_explanation": "Explain why the resume got this ATS score and what would increase it"
}}

Return ONLY the JSON. No extra text, no markdown, no explanation.
"""
    return prompt




def get_jd_match_prompt(resume_text: str, job_description: str) -> str:
    """
    Prompt for JD matching analysis.
    """
    prompt = f"""
You are an expert technical recruiter analyzing resume-to-job fit.

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:2000]}

Analyze the match and respond in this exact JSON format only:

{{
    "match_score": <number 0-100>,
    "match_summary": "2 sentence summary of overall fit",
    "strong_matches": ["skill/experience that matches well 1", "match 2", "match 3"],
    "gaps": ["missing requirement 1", "gap 2", "gap 3"],
    "recommendation": "Should they apply? Why or why not?",
    "tailoring_tips": ["how to tailor resume for this role 1", "tip 2", "tip 3"]
}}

Return ONLY the JSON. No extra text.
"""
    return prompt