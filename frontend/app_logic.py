import streamlit as st
from openai import OpenAI

from utils.config import get_api_key
from utils.pdf_utils import extract_pdf_text, split_into_chunks
from backend.ai_analyzer import analyze_chunk, fuse_partials


def initialize_app():
    """Initialize the application and check API key."""
    api_key = get_api_key()
    if not api_key:
        st.warning("Add your **OPENAI_API_KEY** to `.env` or Streamlit secrets, then reload.")
        st.stop()
    
    client = OpenAI(api_key=api_key)
    return client


def process_resume(client: OpenAI, uploaded_file, target_role: str, model: str):
    """Process the uploaded resume and return analysis results."""
    with st.spinner("Extracting text from PDF…"):
        try:
            resume_text = extract_pdf_text(uploaded_file)
        except Exception as e:
            st.error(f"Could not read PDF. Error: {e}")
            st.stop()

    if not resume_text.strip():
        st.warning("No selectable text found. If your PDF is a scan, run OCR first.")
        st.stop()

    chunks = split_into_chunks(resume_text, max_chars=24000)

    with st.spinner(f"Analyzing ({len(chunks)} chunk{'s' if len(chunks) > 1 else ''})…"):
        partials = [analyze_chunk(client, ch, target_role, model) for ch in chunks]
        result = partials[0] if len(partials) == 1 else fuse_partials(client, partials, target_role, model)

    return result, resume_text
