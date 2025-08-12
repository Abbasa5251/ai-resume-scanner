import os
import streamlit as st
from typing import Optional


def get_api_key() -> Optional[str]:
    """Get OpenAI API key from Streamlit secrets or environment variables."""
    try:
        key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        key = None
    return key or os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = (
    "You are a meticulous career coach and ATS expert. "
    "Given raw resume text, produce concise, recruiter-ready insights. "
    "Be specific, avoid fluff, and keep results practical."
)

USER_TASK_TMPL = """{role_line}
Resume (raw text below):
---
{body}
---
Task:
1) Summarize profile in 2-3 punchy sentences.
2) List 5-8 strengths with evidence from resume.
3) List 3-6 improvement areas (clear, actionable).
4) Give 5 role suggestions (titles) matching skills, most to least aligned.
5) Extract 12-20 top keywords/skills for ATS.
6) Give a tentative ATS-fit score (0-100) for the target role (or general SWE if none).
7) End with a one-line personal brand hook (10-16 words).

Return **valid JSON** with exactly these keys:
- summary (string)
- strengths (string[])
- weaknesses (string[])
- role_suggestions (string[])
- keywords (string[])
- ats_score (number)
- brand_hook (string)
"""
