import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts import get_resume_analysis_prompt, get_jd_match_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model="llama3-8b-8192"


def analyze_resume_with_llm(
    resume_text: str,
    ats_score: float,
    matched_skills: list,
    missing_skills: list,
    job_description: str = ""
) -> dict:
    """
    Sends resume data to Groq LLM.
    Returns structured AI feedback.
    """
    try:
        prompt = get_resume_analysis_prompt(
            resume_text=resume_text,
            ats_score=ats_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            job_description=job_description
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume reviewer. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,     
            max_tokens=2000
        )

        raw_response = response.choices[0].message.content.strip()

        # Clean response and parse JSON
        raw_response = raw_response.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(raw_response)

        return {
            "success": True,
            "analysis": parsed
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": "Failed to parse LLM response",
            "raw": raw_response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def match_jd_with_llm(resume_text: str, job_description: str) -> dict:
    """
    Specific JD matching analysis using LLM.
    """
    try:
        prompt = get_jd_match_prompt(resume_text, job_description)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical recruiter. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )

        raw_response = response.choices[0].message.content.strip()
        raw_response = raw_response.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(raw_response)

        return {
            "success": True,
            "jd_match": parsed
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Failed to parse LLM response"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }