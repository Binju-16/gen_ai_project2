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

st.markdown(
    """
This agent helps synthesize multiple research abstracts or text documents.
It identifies themes, methodologies, conflicts, research gaps, and future research questions.
"""
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input(
        "LLM model",
        os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    mock = st.checkbox(
        "Mock mode (no API calls)",
        value=(os.getenv("MOCK_MODE", "1") == "1")
    )

st.markdown("Paste abstracts or upload text files. Use one abstract per line.")

col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area("Paper abstracts", height=300)

    uploaded = st.file_uploader(
        "Upload text files",
        accept_multiple_files=True,
        type=["txt"]
    )

    example_btn = st.button("Load example abstracts")

    if example_btn:
        text_input = """Paper 1: Machine learning models improved student performance prediction accuracy by 15 percent.
Paper 2: Deep learning models outperformed traditional statistical methods for predicting educational outcomes.
Paper 3: Small sample sizes limited the reliability of student performance prediction studies."""

with col2:
    st.header("Agent Actions")

    st.markdown(
        """
The agent will:

1. Summarize research content  
2. Extract major themes  
3. Identify methodologies  
4. Detect conflicting findings  
5. Identify research gaps  
6. Generate future research questions  
7. Refine output using reviewer feedback  
"""
    )

    run_agent = st.button("Run Research Synthesis Agent")

if run_agent:
    docs = []

    if text_input:
        docs.extend([d.strip() for d in text_input.splitlines() if d.strip()])

    for f in uploaded:
        try:
            docs.append(f.read().decode("utf-8"))
        except Exception:
            st.warning(f"Could not read uploaded file: {f.name}")

    if not docs:
        st.error("Please provide at least one abstract or upload a text file.")
    else:
        prepared = prepare_documents(docs)

        result = summarize_documents(
            prepared,
            SYSTEM_PROMPT,
            FEW_SHOT_EXAMPLES,
            mock=mock,
            model=model
        )

        st.header("Agent Output")

        st.subheader("Research Summary")
        st.write(result.get("research_summary", "No summary generated."))

        st.subheader("Major Themes")
        st.write(result.get("major_themes", []))

        st.subheader("Methodologies")
        st.write(result.get("methodologies", []))

        st.subheader("Conflicting Findings")
        st.write(result.get("conflicting_findings", []))

        st.subheader("Research Gaps")
        st.write(result.get("research_gaps", []))

        st.subheader("Future Research Questions")
        st.write(result.get("future_research_questions", []))

        st.subheader("Confidence Score")
        st.write(result.get("confidence_score", "Not provided"))

        st.subheader("Grounding References")
        st.write(result.get("grounding_refs", []))

        st.warning(
            "Human review is required before using this synthesis for academic or professional decisions."
        )

        st.subheader("Reviewer Feedback")

        feedback = st.text_area(
            "Tell the agent how to improve the synthesis. Example: focus more on limitations, simplify the summary, or generate stronger research questions."
        )

        if st.button("Refine with Feedback"):
            if not feedback.strip():
                st.error("Please enter feedback text.")
            else:
                refined = refine_summary_with_feedback(
                    result,
                    feedback,
                    SYSTEM_PROMPT,
                    mock=mock,
                    model=model
                )

                st.header("Refined Agent Output")

                st.subheader("Refined Research Summary")
                st.write(refined.get("research_summary", "No refined summary generated."))

                st.subheader("Refined Major Themes")
                st.write(refined.get("major_themes", []))

                st.subheader("Refined Methodologies")
                st.write(refined.get("methodologies", []))

                st.subheader("Refined Conflicting Findings")
                st.write(refined.get("conflicting_findings", []))

                st.subheader("Refined Research Gaps")
                st.write(refined.get("research_gaps", []))

                st.subheader("Refined Future Research Questions")
                st.write(refined.get("future_research_questions", []))

                st.subheader("Refined Confidence Score")
                st.write(refined.get("confidence_score", "Not provided"))

                st.subheader("Refined Grounding References")
                st.write(refined.get("grounding_refs", []))

        try:
            with open("BUILDLOG.md", "a", encoding="utf-8") as f:
                f.write("\n---\n")
                f.write("Run: Research Synthesis Agent\n")
                f.write(f"Input documents: {len(docs)}\n")
                f.write(f"Model: {model}\n")
                f.write("Agent tasks: summary, themes, methodologies, conflicts, gaps, research questions\n")
                f.write(json.dumps(result, indent=2) + "\n")
        except Exception:
            pass

st.sidebar.markdown("---")
st.sidebar.markdown("Draft — human review required before any action.")