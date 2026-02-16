from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from resume_parser import extract_text_from_pdf, clean_text
from matcher import analyze

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

@app.get("/")
def home():
    return render_template("index.html", result=None)

@app.post("/analyze")
def analyze_route():
    if "resume" not in request.files:
        return render_template("index.html", result={"summary": "No file uploaded."})

    f = request.files["resume"]
    if not f.filename.lower().endswith(".pdf"):
        return render_template("index.html", result={"summary": "Please upload a PDF resume."})

    _ = secure_filename(f.filename)  # keep safe even though we don't save it

    jd = request.form.get("job_description", "")
    name = request.form.get("name", "").strip()

    resume_text = clean_text(extract_text_from_pdf(f.stream))
    jd_text = clean_text(jd)

    if not resume_text:
        return render_template("index.html", result={"summary": "Could not read text from PDF. Try a text-based PDF."})

    r = analyze(resume_text, jd_text)
    percent = round(r.score * 100, 1)

    summary_lines = []
    if name:
        summary_lines.append(f"Candidate: {name}")
    summary_lines.append(f"Match Score: {percent}%")
    summary_lines.append(f"Resume skills found: {len(r.resume_skills)}")
    summary_lines.append(f"Job skills found: {len(r.jd_skills)}")
    summary_lines.append(f"Missing skills: {len(r.missing_skills)}")
    summary = "\n".join(summary_lines)

    result = {
        "summary": summary,
        "resume_skills": r.resume_skills,
        "missing_skills": r.missing_skills
    }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
