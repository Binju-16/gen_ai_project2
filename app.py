import os
import json
from dotenv import load_dotenv
import streamlit as st

from src.prompt_templates import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES
from src.processor import prepare_documents
from src.llm_wrapper import summarize_documents, refine_summary_with_feedback

load_dotenv()

st.set_page_config(page_title="Research Synthesis Agent", layout="wide")

st.title("Research Synthesis Agent — Draft")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("LLM model (env OPENAI_MODEL)", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    mock = st.checkbox("Mock mode (no API calls)", value=(os.getenv("MOCK_MODE", "1") == "1"))

st.markdown("Paste abstracts or upload text files (one per paper).")

col1, col2 = st.columns([2,1])

with col1:
    text_input = st.text_area("Paper abstracts (one per line)", height=300)
    uploaded = st.file_uploader("Upload text files", accept_multiple_files=True)
    example_btn = st.button("Load example abstracts")
    if example_btn:
        text_input = """Paper A abstract: We study X and find Y.\nPaper B abstract: We propose Z and show W."""

with col2:
    st.header("Actions")
    if st.button("Summarize and Synthesize"):
        docs = []
        if text_input:
            docs.extend([d.strip() for d in text_input.splitlines() if d.strip()])
        for f in uploaded:
            try:
                docs.append(f.read().decode('utf-8'))
            except Exception:
                pass

        if not docs:
            st.error("Please provide at least one abstract or upload files.")
        else:
            prepared = prepare_documents(docs)
            result = summarize_documents(prepared, SYSTEM_PROMPT, FEW_SHOT_EXAMPLES, mock=mock, model=model)
            st.subheader("Structured Summary")
            st.json(result)
            st.subheader("Suggested Dashboard / Next Steps")
            st.code(result.get("dashboard_pseudocode", "(none)"))

            # feedback loop
            st.subheader("Reviewer Feedback")
            feedback = st.text_area("Provide reviewer feedback or corrections to the summary")
            if st.button("Refine with feedback"):
                if not feedback.strip():
                    st.error("Please enter feedback text.")
                else:
                    refined = refine_summary_with_feedback(result, feedback, SYSTEM_PROMPT, mock=mock, model=model)
                    st.subheader("Refined Summary")
                    st.json(refined)

            # append to build log
            try:
                with open("BUILDLOG.md", "a", encoding="utf-8") as f:
                    f.write("\n---\n")
                    f.write(f"Input docs: {len(docs)}\n")
                    f.write("Prompt snapshot: ...\n")
                    f.write(json.dumps(result) + "\n")
            except Exception:
                pass

st.sidebar.markdown("---")
st.sidebar.markdown("Draft — human review required before any action.")
