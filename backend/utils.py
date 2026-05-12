import re


TECH_KEYWORDS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r",

    # ML / AI
    "machine learning", "deep learning", "nlp", "tensorflow",
    "pytorch", "scikit-learn", "keras", "xgboost",

    # Data
    "pandas", "numpy", "sql", "mysql", "postgresql",
    "mongodb", "spark", "hadoop",

    # Web
    "react", "fastapi", "flask", "django", "node.js",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes",

    # Tools
    "git", "github", "linux", "tableau", "power bi"
}


def extract_keywords(text: str) -> list:
    """
    Extract only meaningful technical keywords.
    """

    text = text.lower()

    found_keywords = []

    for keyword in TECH_KEYWORDS:
        if keyword in text:
            found_keywords.append(keyword)

    return list(set(found_keywords))


def format_response(data: dict) -> dict:
    """
    Standardizes API response format.
    """
    return {
        "success": True,
        "data": data
    }