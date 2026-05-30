# Research Synthesis Agent — Project 2 (Draft)

This repository contains a Streamlit prototype for a Research Synthesis Agent: upload or paste paper abstracts, get structured summaries, cluster themes, and iterate via reviewer feedback.

Quick start

1. Copy `.env.template` to `.env` and add your `OPENAI_API_KEY` (or set `MOCK_MODE=1` to run without a key).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run locally:

```bash
streamlit run app.py
```

Notes
- This is an early scaffold implementing the UI and prompt/LLM wrappers. Next: grounding retrieval, evaluation harness, and deployment to Streamlit Cloud.
# gen_ai_project2
AI application that combines reasoning, planning, and tool usage to solve user defined tasks
