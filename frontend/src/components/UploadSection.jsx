
import { useState } from "react";
import API from "../services/api";

function UploadSection() {

  const [file, setFile] = useState(null);

  const [jobDescription, setJobDescription] = useState("");

  const [result, setResult] = useState(null);

  const [jdMatchResult, setJdMatchResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {

    if (!file) {
      alert("Please upload a PDF resume.");
      return;
    }
    if (!jobDescription.trim()) {
  alert("Please enter a job description.");
  return;
}

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      formData.append("job_description", jobDescription);

      const [analyzeResponse, jdMatchResponse] =
        await Promise.all([

          API.post(
            "/analyze-resume",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          ),

          API.post(
            "/match-jd",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )

        ]);

      setResult(analyzeResponse.data.data);

      setJdMatchResult(jdMatchResponse.data.data);

    } catch (error) {

      console.error(error);

      alert("Something went wrong");

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">

      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">

          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            AI Resume Analyzer
          </h1>

          <p className="text-gray-600 text-lg">
            Upload your resume and have AI-assisted resume analysis with ATS scoring and job fit insights.
          </p>

        </div>


        {/* Upload Section */}
        <div className="bg-white shadow-xl rounded-3xl p-8 mb-10">

          {/* Upload */}
          <div className="mb-6">

            <label className="block mb-2 font-semibold text-gray-700">
              Upload Resume (PDF)
            </label>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full border rounded-xl p-4 bg-gray-50"
            />

          </div>


          {/* Job Description */}
          <div className="mb-6">

            <label className="block mb-2 font-semibold text-gray-700">
              Job Description
            </label>

            <textarea
              rows="8"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
              className="w-full border rounded-xl p-4 bg-gray-50"
            />

          </div>


          {/* Button */}
          <button
            onClick={handleSubmit}
            className="w-full bg-black text-white py-4 rounded-2xl font-semibold text-lg hover:bg-gray-800 transition"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>

        </div>


        {/* Results */}
        {result && (

          <div className="space-y-8">

            {/* Top Score Cards */}
            <div className="grid md:grid-cols-2 gap-6">

              {/* ATS Score */}
              <div className="bg-white shadow-xl rounded-3xl p-8 border border-gray-100">

                <h2 className="text-xl font-bold text-gray-700 mb-4">
                  ATS Score
                </h2>

                <div className="text-7xl font-bold text-blue-600 mb-4">
                  {result.ats_result.overall_score}
                </div>

                <p className="text-gray-500 leading-7">
                  Resume optimization score based on ATS analysis.
                </p>

              </div>


              {/* JD Match Score */}
              {jdMatchResult && (

                <div className="bg-white shadow-xl rounded-3xl p-8 border border-gray-100">

                  <h2 className="text-xl font-bold text-gray-700 mb-4">
                    Job Match Score
                  </h2>

                  <div className="text-7xl font-bold text-green-600 mb-4">
                    {jdMatchResult.jd_match.jd_match.match_score}%
                  </div>

                  <p className="text-gray-500 leading-7">
                    AI-powered resume and job description compatibility analysis.
                  </p>

                </div>

              )}

            </div>


            {/* Skills Section */}
            <div className="grid md:grid-cols-2 gap-6">

              {/* Matched Skills */}
              <div className="bg-white shadow-lg rounded-3xl p-6">

                <h3 className="text-2xl font-bold mb-5 text-green-700">
                  Matched Skills
                </h3>

                <div className="flex flex-wrap gap-3">

                  {result.ats_result.matched_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}

                </div>

              </div>


              {/* Missing Skills */}
              <div className="bg-white shadow-lg rounded-3xl p-6">

                <h3 className="text-2xl font-bold mb-5 text-red-700">
                  Missing Skills
                </h3>

                <div className="flex flex-wrap gap-3">

                  {result.ats_result.missing_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-red-100 text-red-800 px-4 py-2 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}

                </div>

              </div>

            </div>


            {/* AI Feedback */}
            {result.llm_analysis.success && (

              <div className="bg-white shadow-lg rounded-3xl p-8">

                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  AI Resume Feedback
                </h2>

                <p className="text-gray-700 leading-8 mb-8 text-lg">
                  {result.llm_analysis.analysis.overall_feedback}
                </p>

                <div>

                  <h3 className="font-bold text-xl mb-5">
                    Suggested Improvements
                  </h3>

                  <ul className="space-y-4">

                    {result.llm_analysis.analysis.improvements.map(
                      (item, index) => (
                        <li
                          key={index}
                          className="bg-gray-50 rounded-2xl p-5"
                        >
                          • {item}
                        </li>
                      )
                    )}

                  </ul>

                </div>

              </div>

            )}


            {/* JD Match Analysis */}
            {jdMatchResult && (

              <div className="bg-white shadow-lg rounded-3xl p-8">

                <h2 className="text-3xl font-bold mb-8 text-gray-800">
                  Resume ↔ Job Fit Analysis
                </h2>


                {/* Match Summary */}
                <div className="mb-8">

                  <h3 className="font-bold text-xl mb-4">
                    Match Summary
                  </h3>

                  <p className="text-gray-700 leading-8 text-lg">
                    {jdMatchResult.jd_match.jd_match.match_summary}
                  </p>

                </div>


                {/* Strong Matches + Gaps */}
                <div className="grid md:grid-cols-2 gap-8 mb-10">

                  {/* Strong Matches */}
                  <div>

                    <h3 className="font-bold text-xl mb-5 text-green-700">
                      Strong Matches
                    </h3>

                    <div className="space-y-4">

                      {jdMatchResult.jd_match.jd_match.strong_matches.map(
                        (item, index) => (
                          <div
                            key={index}
                            className="bg-green-50 border border-green-100 rounded-2xl p-5"
                          >
                            ✓ {item}
                          </div>
                        )
                      )}

                    </div>

                  </div>


                  {/* Gaps */}
                  <div>

                    <h3 className="font-bold text-xl mb-5 text-red-700">
                      Gaps
                    </h3>

                    <div className="space-y-4">

                      {jdMatchResult.jd_match.jd_match.gaps.map(
                        (item, index) => (
                          <div
                            key={index}
                            className="bg-red-50 border border-red-100 rounded-2xl p-5"
                          >
                            ✗ {item}
                          </div>
                        )
                      )}

                    </div>

                  </div>

                </div>


                {/* Recommendation */}
                <div className="mb-10">

                  <h3 className="font-bold text-xl mb-4">
                    Recommendation
                  </h3>

                  <div className="bg-blue-50 border border-blue-100 rounded-3xl p-6 text-gray-700 leading-8 text-lg">
                    {jdMatchResult.jd_match.jd_match.recommendation}
                  </div>

                </div>


                {/* Tailoring Tips */}
                <div>

                  <h3 className="font-bold text-xl mb-5">
                    Tailoring Tips
                  </h3>

                  <ul className="space-y-4">

                    {jdMatchResult.jd_match.jd_match.tailoring_tips.map(
                      (tip, index) => (
                        <li
                          key={index}
                          className="bg-gray-50 rounded-2xl p-5"
                        >
                          • {tip}
                        </li>
                      )
                    )}

                  </ul>

                </div>

              </div>

            )}

          </div>

        )}

      </div>

    </div>
  );
}

export default UploadSection;

