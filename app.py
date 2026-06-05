import os
import json
from dotenv import load_dotenv
import streamlit as st

from src.prompt_templates import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES
from src.processor import prepare_documents
from src.llm_wrapper import summarize_documents, refine_summary_with_feedback

load_dotenv()

st.set_page_config(page_title="Research Synthesis Agent", layout="wide")

st.title("Research Synthesis Agent ")

st.markdown(
    """
This agent helps synthesize multiple research abstracts or text documents.
It identifies themes, methodologies, conflicts, research gaps, and future research questions.
"""
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("LLM model", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
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

1. Analyze uploaded research
2. Decide whether additional information is needed
3. Invoke available tools when appropriate
4. Generate a structured synthesis
5. Identify themes and methodologies
6. Detect conflicts and research gaps
7. Generate future research questions
8. Accept reviewer feedback
9. Revise the synthesis 
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
        docs.append(
            "No research document was provided. Please use the fetch_sample_abstract tool to retrieve a sample abstract about research_synthesis."
        )

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
    themes = result.get("major_themes", [])
    if themes:
        for item in themes:
            st.write(f"- {item}")
    else:
        st.write("No major themes identified.")

    st.subheader("Methodologies")
    methodologies = result.get("methodologies", [])
    if methodologies:
        for item in methodologies:
            st.write(f"- {item}")
    else:
        st.write("No methodologies identified.")

    st.subheader("Conflicting Findings")
    conflicts = result.get("conflicting_findings", [])
    if conflicts:
        for item in conflicts:
            st.write(f"- {item}")
    else:
        st.write("No conflicting findings detected.")

    st.subheader("Research Gaps")
    gaps = result.get("research_gaps", [])
    if gaps:
        for item in gaps:
            st.write(f"- {item}")
    else:
        st.write("No research gaps identified.")

    st.subheader("Future Research Questions")
    questions = result.get("future_research_questions", [])
    if questions:
        for item in questions:
            st.write(f"- {item}")
    else:
        st.write("No future research questions generated.")

    st.subheader("Confidence Score")
    st.write(result.get("confidence_score", "Not provided"))

    st.subheader("Tools Used")
    tools_used = list(set(result.get("tools_used", [])))

if tools_used:
    for tool in tools_used:
        st.success(f"Tool called: {tool}")
    else:
        st.info("No tool was called for this run.")

    st.subheader("Grounding References")
    refs = [
    ref for ref in result.get("grounding_refs", [])
    if isinstance(ref, int) and ref < len(prepared)
]

    if refs:
        for ref in refs:
            try:
                ref_index = int(ref)
                st.markdown(f"### Document {ref_index + 1}")

                if ref_index < len(prepared):
                    preview = prepared[ref_index]["text"][:500]
                    st.info(preview + ("..." if len(prepared[ref_index]["text"]) > 500 else ""))
                else:
                    st.warning(f"Document reference {ref_index} was returned, but no matching document was found.")
            except Exception:
                st.warning(f"Invalid grounding reference: {ref}")
    else:
        st.write("No grounding references provided.")

    st.subheader("Source Documents Used")

    for doc in prepared:
        with st.expander(f"Document {doc['id'] + 1}"):
            st.write(doc["text"])

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
            refined_themes = refined.get("major_themes", [])
            if refined_themes:
                for item in refined_themes:
                    st.write(f"- {item}")
            else:
                st.write("No refined themes generated.")

            st.subheader("Refined Methodologies")
            refined_methods = refined.get("methodologies", [])
            if refined_methods:
                for item in refined_methods:
                    st.write(f"- {item}")
            else:
                st.write("No refined methodologies generated.")

            st.subheader("Refined Conflicting Findings")
            refined_conflicts = refined.get("conflicting_findings", [])
            if refined_conflicts:
                for item in refined_conflicts:
                    st.write(f"- {item}")
            else:
                st.write("No refined conflicting findings generated.")

            st.subheader("Refined Research Gaps")
            refined_gaps = refined.get("research_gaps", [])
            if refined_gaps:
                for item in refined_gaps:
                    st.write(f"- {item}")
            else:
                st.write("No refined research gaps generated.")

            st.subheader("Refined Future Research Questions")
            refined_questions = refined.get("future_research_questions", [])
            if refined_questions:
                for item in refined_questions:
                    st.write(f"- {item}")
            else:
                st.write("No refined future research questions generated.")

            st.subheader("Refined Confidence Score")
            st.write(refined.get("confidence_score", "Not provided"))

            st.subheader("Tools Used During Refinement")
            refined_tools_used = refined.get("tools_used", [])

            if refined_tools_used:
                for tool in refined_tools_used:
                    st.success(f"Tool called: {tool}")
            else:
                st.info("No tool was called during refinement.")

    try:
        with open("BUILDLOG.md", "a", encoding="utf-8") as f:
            f.write("\n---\n")
            f.write("Run: Research Synthesis Agent\n")
            f.write(f"Input documents: {len(docs)}\n")
            f.write(f"Model: {model}\n")
            f.write("Agent tasks: summary, themes, methodologies, conflicts, gaps, research questions\n")
            f.write(f"Tools used: {result.get('tools_used', [])}\n")
            f.write(json.dumps(result, indent=2) + "\n")
    except Exception:
        pass

st.sidebar.markdown("---")
st.sidebar.markdown("Human review required before academic or professional use.")