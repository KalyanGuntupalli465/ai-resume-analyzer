import re
from utils import extract_keywords

# Common technical skills
COMMON_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "go", "rust", "kotlin", "swift",

    # ML / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "hugging face", "langchain", "llm", "transformers",

    # Data
    "pandas", "numpy", "sql", "mysql", "postgresql", "mongodb",
    "spark", "hadoop", "airflow", "dbt", "snowflake",

    # Web / Backend
    "react", "fastapi", "flask", "django", "node.js", "rest api",
    "graphql", "docker", "kubernetes",

    # Cloud / MLOps
    "aws", "gcp", "azure", "mlflow", "ci/cd", "git", "github",
    "linux", "terraform",

]

# Skill inference mapping
RELATED_SKILLS = {
    "machine learning": ["scikit-learn", "pandas", "numpy"],
    "data analytics": ["pandas", "numpy", "sql"],
    "deep learning": ["tensorflow", "pytorch"],
    "nlp": ["transformers", "hugging face"],
    "power bi": ["tableau"],
    "react.js": ["javascript"],
}


def calculate_ats_score(resume_text: str, job_description: str = "") -> dict:
    """
    Main ATS scoring function.
    """

    resume_text_lower = resume_text.lower()

    # 1. Skill Match
    skill_score, matched_skills, missing_skills = calculate_skill_score(
        resume_text_lower,
        job_description
    )

    # 2. Keyword Match
    keyword_score, matched_keywords, missing_keywords = calculate_keyword_score(
        resume_text_lower,
        job_description.lower()
    )

    # 3. Experience Score
    experience_score = calculate_experience_score(resume_text_lower)

    # 4. Education Score
    education_score = calculate_education_score(resume_text_lower)

    # Final Weighted Score
    overall_score = (
        (skill_score * 0.50) +
        (keyword_score * 0.20) +
        (experience_score * 0.20) +
        (education_score * 0.10)
    )

    return {
        "overall_score": round(overall_score, 1),

        "breakdown": {
            "skill_match": round(skill_score, 1),
            "keyword_overlap": round(keyword_score, 1),
            "experience_relevance": round(experience_score, 1),
            "education_match": round(education_score, 1)
        },

        "matched_skills": matched_skills,

        "missing_skills": missing_skills[:10],

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords[:10]
    }


def calculate_skill_score(
    resume_text: str,
    job_description: str = ""
) -> tuple:
    """
    Dynamic ATS skill scoring with inferred skills.
    """

    matched = []
    missing = []

    score = 0

    # If JD exists → role-aware scoring
    if job_description.strip():

        jd_lower = job_description.lower()

        jd_skills = [
            skill for skill in COMMON_SKILLS
            if skill in jd_lower
        ]

        # No technical skills found
        if len(jd_skills) == 0:
            return 70.0, [], []

        for skill in jd_skills:

            # Direct skill match
            if skill in resume_text:
                matched.append(skill)

            else:
                inferred = False

                # Inferred skill matching
                for base_skill, related_skills in RELATED_SKILLS.items():

                    if (
                        skill in related_skills
                        and base_skill in resume_text
                    ):
                        matched.append(skill + " (inferred)")
                        inferred = True
                        break

                if not inferred:
                    missing.append(skill)

        score = (len(matched) / len(jd_skills)) * 100

    # General resume scoring
    else:

        for skill in COMMON_SKILLS:
            if skill in resume_text:
                matched.append(skill)

        score = min(len(matched) * 8, 100)

        missing = [
            skill for skill in COMMON_SKILLS
            if skill not in matched
        ]

    return round(score, 1), matched, missing


def calculate_keyword_score(
    resume_text: str,
    job_description: str
) -> tuple:
    """
    Technical keyword matching between JD and resume.
    """

    if not job_description.strip():
        return 75.0, [], []

    jd_keywords = extract_keywords(job_description)

    resume_keywords = extract_keywords(resume_text)

    matched = [
        kw for kw in jd_keywords
        if kw in resume_keywords
    ]

    missing = [
        kw for kw in jd_keywords
        if kw not in resume_keywords
    ]

    if len(jd_keywords) == 0:
        return 75.0, [], []

    score = (len(matched) / len(jd_keywords)) * 100

    return round(score, 1), matched, missing


def calculate_experience_score(resume_text: str) -> float:
    """
    Experience scoring logic.
    """

    score = 0

    # Years of experience patterns
    year_patterns = [
        r'\d+\+?\s*years?\s*of\s*experience',
        r'experience\s*of\s*\d+\+?\s*years?',
        r'\d+\+?\s*years?\s*experience'
    ]

    for pattern in year_patterns:
        if re.search(pattern, resume_text):
            score += 30
            break

    # Action verbs
    action_verbs = [
        "developed", "built", "designed", "implemented",
        "led", "managed", "created", "optimized",
        "deployed", "engineered", "architected",
        "improved", "reduced", "increased",
        "delivered", "analyzed", "trained",
        "evaluated", "researched", "collaborated",
        "automated", "predicted"
    ]

    verb_count = sum(
        1 for verb in action_verbs
        if verb in resume_text
    )

    score += min(verb_count * 5, 40)

    # Projects / internships
    if any(
        word in resume_text
        for word in ["project", "internship", "intern"]
    ):
        score += 20

    # Metrics / numbers
    if re.search(r'\d+%|\$\d+|\d+x', resume_text):
        score += 10

    return min(score, 100)


def calculate_education_score(resume_text: str) -> float:
    """
    Education scoring logic.
    """

    score = 0

    # Degree level
    if any(
        word in resume_text
        for word in ["ph.d", "phd", "doctorate"]
    ):
        score += 100

    elif any(
        word in resume_text
        for word in ["master", "m.s", "m.sc", "msc", "ms "]
    ):
        score += 85

    elif any(
        word in resume_text
        for word in ["bachelor", "b.s", "b.sc", "bsc", "b.tech", "be "]
    ):
        score += 70

    elif any(
        word in resume_text
        for word in ["associate", "diploma"]
    ):
        score += 50

    # Relevant field bonus
    if any(
        field in resume_text
        for field in [
            "computer science",
            "software engineering",
            "data science",
            "artificial intelligence",
            "machine learning",
            "information technology"
        ]
    ):
        score = min(score + 15, 100)

    return float(score)