from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_text_from_pdf
from utils import extract_keywords, format_response
from scoring import calculate_ats_score
from analyzer import analyze_resume_with_llm, match_jd_with_llm
import io

app = FastAPI(title="AI Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://ai-resume-analyzer-53c3vrjlc-mohan-kalyan-guntupallis-projects.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"AI Resume Analyzer API is running!"}


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    contents = await file.read()
    file_like = io.BytesIO(contents)
    extracted_text = extract_text_from_pdf(file_like)
    keywords = extract_keywords(extracted_text)

    return format_response({
        "filename": file.filename,
        "extracted_text": extracted_text[:500],
        "keywords": keywords[:30],
        "total_keywords": len(keywords)
    })


@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(default="")
):
  
    contents = await file.read()
    file_like = io.BytesIO(contents)

    # Step 1: Extracting text
    extracted_text = extract_text_from_pdf(file_like)

    # Step 2: ATS Score (deterministic)
    ats_result = calculate_ats_score(extracted_text, job_description)

    # Step 3: LLM Analysis (AI layer)
    llm_result = analyze_resume_with_llm(
        resume_text=extracted_text,
        ats_score=ats_result["overall_score"],
        matched_skills=ats_result["matched_skills"],
        missing_skills=ats_result["missing_skills"],
        job_description=job_description
    )

    return format_response({
        "filename": file.filename,
        "ats_result": ats_result,
        "llm_analysis": llm_result,
        "text_preview": extracted_text[:300]
    })


@app.post("/match-jd")
async def match_jd(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Specific JD matching endpoint.
    """
    contents = await file.read()
    file_like = io.BytesIO(contents)

    extracted_text = extract_text_from_pdf(file_like)
    jd_match = match_jd_with_llm(extracted_text, job_description)

    return format_response({
        "filename": file.filename,
        "jd_match": jd_match
    })