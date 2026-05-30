import os
import json
from typing import List

try:
    import openai
except Exception:
    openai = None

def _mock_summarize(prepared):
    # Return a simple mocked structured summary
    summaries = []
    for item in prepared:
        summaries.append({"text": item["text"][:200], "grounding_refs": [item["id"]]})
    return {
        "title": "Mock Synthesis",
        "summaries": summaries,
        "themes": ["theme_placeholder"],
        "gaps": [],
        "dashboard_pseudocode": "# pseudocode: display summary list and theme counts",
        "confidence": 0.5,
        "grounding_refs": [p["id"] for p in prepared]
    }

def summarize_documents(prepared: List[dict], system_prompt: str, few_shot: List[dict], mock: bool = True, model: str = None):
    if mock or os.getenv("MOCK_MODE", "1") == "1":
        return _mock_summarize(prepared)

    # Build prompt
    messages = [{"role":"system","content":system_prompt},
                {"role":"user","content": "Summarize the following documents: " + json.dumps(prepared)}]
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _mock_summarize(prepared)
    openai.api_key = api_key
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.0)
    text = resp["choices"][0]["message"]["content"]
    try:
        return json.loads(text)
    except Exception:
        return {"raw": text}

def refine_summary_with_feedback(summary: dict, feedback: str, system_prompt: str, mock: bool = True, model: str = None):
    if mock or os.getenv("MOCK_MODE", "1") == "1":
        # naive mock: append feedback to title
        s = dict(summary)
        s["title"] = s.get("title", "") + " (refined)"
        return s

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return refine_summary_with_feedback(summary, feedback, system_prompt, mock=True)
    openai.api_key = api_key
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    messages = [
        {"role":"system","content": system_prompt},
        {"role":"user","content": "Existing summary: " + json.dumps(summary) + "\nReviewer feedback: " + feedback}
    ]
    resp = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.0)
    text = resp["choices"][0]["message"]["content"]
    try:
        return json.loads(text)
    except Exception:
        return {"raw": text}
