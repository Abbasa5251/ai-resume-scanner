import streamlit as st
import json
from typing import Dict, Any


def render_header():
    """Render the main header section."""
    st.set_page_config(page_title="ADev AI Resume Analyzer", page_icon="🧠", layout="centered")
    st.title("🧠 ADev AI Resume Analyzer")
    st.caption("Upload a PDF, choose a target role, and get a recruiter-ready analysis.")


def render_input_section():
    """Render the input controls section."""
    colA, colB = st.columns([2, 1])
    with colA:
        target_role = st.text_input(
            "Target role (optional)", 
            value="Full-Stack Developer (Python + JavaScript)"
        )
    with colB:
        model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    
    uploaded = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    return target_role, model, uploaded


def render_analysis_button(uploaded):
    """Render the analyze button."""
    return st.button("Analyze Resume", type="primary", disabled=uploaded is None)


def render_results(result: Dict[str, Any], resume_text: str):
    """Render the analysis results."""
    # Summary
    st.subheader("📌 Summary")
    st.write(result.get("summary", "N/A"))

    # Strengths and Weaknesses
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ Strengths")
        for s in result.get("strengths", [])[:8]:
            st.markdown(f"- {s}")
    with c2:
        st.subheader("🧯 Improvement Areas")
        for w in result.get("weaknesses", [])[:6]:
            st.markdown(f"- {w}")

    # Role Suggestions
    st.subheader("🎯 Role Suggestions")
    for r in result.get("role_suggestions", []):
        st.markdown(f"- {r}")

    # Keywords
    st.subheader("🔑 Keywords for ATS")
    st.markdown(", ".join(result.get("keywords", [])))

    # ATS Score
    st.subheader("📈 ATS Fit (tentative)")
    st.metric("Score", str(result.get("ats_score", "N/A")))

    # Brand Hook
    st.subheader("🪪 Personal Brand Hook")
    st.write(result.get("brand_hook", "N/A"))

    # Download Section
    st.divider()
    st.subheader("Downloads")
    st.download_button(
        "⬇️ Full JSON",
        data=json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="resume_ai_review.json",
        mime="application/json",
    )
    st.download_button(
        "⬇️ Raw Resume Text",
        data=resume_text.encode("utf-8"),
        file_name="resume_text.txt",
        mime="text/plain",
    )

    st.success("Done! 🎉")


def render_footer():
    """Render the footer."""
    st.markdown(
      f"<p style='text-align: center; color: gray; font-size: 0.85rem;'>"
      f"Built by <a href='https://github.com/Abbasa5251' target='_blank'>ADev</a> 💙"
      f"</p>",
      unsafe_allow_html=True
    )
