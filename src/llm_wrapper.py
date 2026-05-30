import os
import json
from typing import List

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def _mock_summarize(prepared):
    grounding_refs = [p["id"] for p in prepared]
    combined_text = " ".join([p["text"] for p in prepared])

    return {
        "research_summary": (
            "This draft synthesis is based on the provided research text. "
            "The documents appear to discuss technical or academic findings that require deeper review."
        ),
        "major_themes": [
            "Research problem and motivation",
            "Methodological approach",
            "Findings and implications"
        ],
        "methodologies": [
            "Document-based analysis",
            "Research synthesis",
            "Comparative review"
        ],
        "conflicting_findings": [
            "No clear conflicting findings were detected from the provided text alone."
        ],
        "research_gaps": [
            "More documents may be needed to identify stronger research gaps.",
            "The current synthesis is limited by the amount and detail of the uploaded text."
        ],
        "future_research_questions": [
            "What patterns appear across a larger set of papers?",
            "Which methods produce the most reliable findings?",
            "What limitations are repeated across the literature?"
        ],
        "confidence_score": 0.55 if len(combined_text) < 1000 else 0.75,
        "grounding_refs": grounding_refs
    }


def summarize_documents(
    prepared: List[dict],
    system_prompt: str,
    few_shot: List[dict],
    mock: bool = True,
    model: str = None
):
    if mock or os.getenv("MOCK_MODE", "1") == "1":
        return _mock_summarize(prepared)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return _mock_summarize(prepared)

    client = OpenAI(api_key=api_key)
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Analyze the following research documents. "
                "Return only valid JSON using the required schema.\n\n"
                f"Few-shot examples:\n{json.dumps(few_shot, indent=2)}\n\n"
                f"Documents:\n{json.dumps(prepared, indent=2)}"
            )
        }
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0
    )

    text = resp.choices[0].message.content

    try:
        return json.loads(text)
    except Exception:
        return {
            "research_summary": text,
            "major_themes": [],
            "methodologies": [],
            "conflicting_findings": [],
            "research_gaps": [],
            "future_research_questions": [],
            "confidence_score": 0.3,
            "grounding_refs": []
        }


def refine_summary_with_feedback(
    summary: dict,
    feedback: str,
    system_prompt: str,
    mock: bool = True,
    model: str = None
):
    if mock or os.getenv("MOCK_MODE", "1") == "1":
        refined = dict(summary)
        refined["research_summary"] = (
            refined.get("research_summary", "")
            + f" Refined based on reviewer feedback: {feedback}"
        )
        refined["confidence_score"] = min(
            float(refined.get("confidence_score", 0.5)) + 0.05,
            1.0
        )
        return refined

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return refine_summary_with_feedback(summary, feedback, system_prompt, mock=True)

    client = OpenAI(api_key=api_key)
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Revise the existing research synthesis based on the reviewer feedback. "
                "Return only valid JSON using the required schema.\n\n"
                f"Existing synthesis:\n{json.dumps(summary, indent=2)}\n\n"
                f"Reviewer feedback:\n{feedback}"
            )
        }
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0
    )

    text = resp.choices[0].message.content

    try:
        return json.loads(text)
    except Exception:
        return {
            "research_summary": text,
            "major_themes": [],
            "methodologies": [],
            "conflicting_findings": [],
            "research_gaps": [],
            "future_research_questions": [],
            "confidence_score": 0.3,
            "grounding_refs": []
        }