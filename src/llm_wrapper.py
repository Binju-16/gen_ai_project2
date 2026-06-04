import os
import json
from typing import List

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from src.tools import fetch_sample_abstract


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_sample_abstract",
            "description": (
                "Fetch a built-in sample research abstract when the user asks for an example, "
                "does not provide enough research text, or needs a sample topic to analyze."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "The research topic to fetch. "
                            "Options: education_ai, research_synthesis, healthcare_ai."
                        ),
                        "enum": [
                            "education_ai",
                            "research_synthesis",
                            "healthcare_ai"
                        ]
                    }
                },
                "required": ["topic"],
                "additionalProperties": False
            }
        }
    }
]


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
        "grounding_refs": grounding_refs,
        "tools_used": ["mock_mode"]
    }


def _safe_json_loads(text: str) -> dict:
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
            "grounding_refs": [],
            "tools_used": []
        }


def _execute_tool_call(tool_call):
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments or "{}")

    if function_name == "fetch_sample_abstract":
        topic = arguments.get("topic", "research_synthesis")
        tool_result = fetch_sample_abstract(topic)

        return {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(tool_result)
        }

    return {
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": json.dumps({"error": f"Unknown tool: {function_name}"})
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
                "If the documents are missing, too short, or the user appears to need an example, "
                "you may call the fetch_sample_abstract tool before producing the final synthesis. "
                "Return only valid JSON using the required schema. "
                "Include a tools_used field listing any tools called.\n\n"
                f"Few-shot examples:\n{json.dumps(few_shot, indent=2)}\n\n"
                f"Documents:\n{json.dumps(prepared, indent=2)}"
            )
        }
    ]

    first_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.0
    )

    first_message = first_response.choices[0].message

    if first_message.tool_calls:
        messages.append(first_message)

        tools_used = []

        for tool_call in first_message.tool_calls:
            tools_used.append(tool_call.function.name)
            messages.append(_execute_tool_call(tool_call))

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0
        )

        text = final_response.choices[0].message.content
        parsed = _safe_json_loads(text)
        parsed["tools_used"] = tools_used
        return parsed

    text = first_message.content
    parsed = _safe_json_loads(text)
    parsed.setdefault("tools_used", [])
    return parsed


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
        refined["tools_used"] = refined.get("tools_used", []) + ["mock_feedback_refinement"]
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
                "Return only valid JSON using the required schema. "
                "Include a tools_used field.\n\n"
                f"Existing synthesis:\n{json.dumps(summary, indent=2)}\n\n"
                f"Reviewer feedback:\n{feedback}"
            )
        }
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.0
    )

    message = resp.choices[0].message

    if message.tool_calls:
        messages.append(message)

        tools_used = []

        for tool_call in message.tool_calls:
            tools_used.append(tool_call.function.name)
            messages.append(_execute_tool_call(tool_call))

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0
        )

        text = final_response.choices[0].message.content
        parsed = _safe_json_loads(text)
        parsed["tools_used"] = tools_used
        return parsed

    text = message.content
    parsed = _safe_json_loads(text)
    parsed.setdefault("tools_used", [])
    return parsed