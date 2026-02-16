from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set, Dict
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Keep this list small + job-relevant; expand later
SKILLS = sorted({
    "python","java","c#","javascript","sql","mysql","postgresql","mongodb",
    "asp.net","asp.net web forms","flask","django","spring boot","rest","apis",
    "git","github","docker","aws","linux","html","css","react","node.js",
    "sql server","oracle","microservices","unit testing","jwt","oauth",
    "data structures","oops","nlp","machine learning"
})

def _normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9\.\+#\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_skills(text: str) -> List[str]:
    t = _normalize(text)
    found: Set[str] = set()
    for s in SKILLS:
        # match whole word-ish
        pattern = r"\b" + re.escape(s) + r"\b"
        if re.search(pattern, t):
            found.add(s)
    return sorted(found)

def match_score(resume_text: str, jd_text: str) -> float:
    docs = [_normalize(resume_text), _normalize(jd_text)]
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(docs)
    score = cosine_similarity(X[0:1], X[1:2])[0][0]
    return float(score)

@dataclass
class AnalysisResult:
    score: float
    resume_skills: List[str]
    jd_skills: List[str]
    missing_skills: List[str]

def analyze(resume_text: str, jd_text: str) -> AnalysisResult:
    rs = extract_skills(resume_text)
    js = extract_skills(jd_text)
    missing = sorted(set(js) - set(rs))
    score = match_score(resume_text, jd_text)

    return AnalysisResult(
        score=score,
        resume_skills=rs,
        jd_skills=js,
        missing_skills=missing
    )
