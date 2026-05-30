# Project 2 — Roadmap: Autonomous, Tool-Using AI for Policy/Rule Updates

1. Project context
------------------
- Build a small, demonstrable AI system that ingests policy or rule updates (plain text or spreadsheet-style rows), summarizes the change into structured fields, and suggests dashboard logic or pseudo-code for human review.
- Emphasis: autonomy in analysis and tool use (file handling, summarization), but with mandatory human-in-the-loop review.

2. Problem statement
--------------------
- Organizations need a safe, auditable way to apply policy/rule updates. Manual triage is slow and error-prone. We propose a lightweight assistant that converts freeform updates into structured summaries and suggested actions while grounding outputs in uploaded policy text.

3. Target user
----------------
- Product managers, compliance officers, or developer-operators who receive policy/rule changes and need a fast, auditable summary and suggested dashboard logic to implement and review.

4. MVP scope for this week
-------------------------
- Single-page web prototype (Streamlit or Gradio) with:
  - Textbox to paste a policy/rule update.
  - Optional example input prefilled.
  - Button to upload a policy file (text/CSV/TSV) used for grounding.
  - AI-generated structured summary (JSON-like fields).
  - Suggested dashboard logic or pseudo-code snippet.
  - Human-review warning and “confidence” estimate.
  - Minimal logging of prompts and outputs for the build log.

5. Out-of-scope items for the draft
----------------------------------
- Full RBAC, automated enforcement, or live integrations with production dashboards.
- Complex multi-agent orchestration, real-time streaming, or expensive fine-tuning.

6. Recommended tech stack
-------------------------
- Prototype (simplest): Streamlit (Python) or Gradio — both are beginner-friendly and deploy to free hosting quickly.
- Backend logic: Python 3.10+, `requests` or `httpx`, `pandas` (optional for CSV), `python-dotenv` for secrets.
- LLM access: OpenAI-compatible API or Hugging Face Inference endpoints; for a no-cost path, use local or HF-hosted open models (or the community `text-generation` endpoints).
- Repo: GitHub with clear commits.

7. Hosting/deployment plan
-------------------------
- Easiest: Streamlit Cloud (free tier) or Hugging Face Spaces (Gradio/Streamlit). Both support public URLs quickly.
- Alternative: Deploy a small Flask app to Render or Railway (free tiers available), or host on Vercel/Netlify with serverless functions.

8. System prompt design
------------------------
- Purposeful, concise system prompt to set role, constraints, grounding priority, and safety rules. Example elements:
  - Role: assistant that ingests policy/rule updates and returns a structured summary and suggested dashboard logic.
  - Constraints: do NOT auto-enact changes, always include a human-review warning, cite grounding sources by filename/row index.
  - Output format: JSON with fields `title`, `change_type`, `affected_entities`, `summary`, `suggested_checks`, `dashboard_pseudocode`, `confidence`, `grounding_refs`.

9. Prompt engineering techniques to use
-------------------------------------
- Chain-of-thought suppression for deterministic outputs (use `format`/`system` instructions to avoid extra reasoning text).
- Few-shot examples showing input → desired structured JSON.
- Output schema enforcement (explicit JSON schema in prompt). Provide positive and negative examples.
- Temperature control: low temperature (0–0.2) for deterministic summaries; experiment with higher for alternative phrasing.
- Prompt snapshot logging: save prompt + system prompt + grounding snippet for reproducibility.

10. Grounding strategy
----------------------
- Accept uploaded policy text or CSV/TSV. Preprocess into numbered paragraphs or rows.
- When calling the LLM, include only relevant slices (max token aware) and always instruct the model to cite the exact paragraph/row index used as grounding.
- For larger policies, implement a simple retrieval step: convert paragraphs/rows to embeddings (optional) and retrieve top-k, or use naive keyword matching for the MVP.

11. Coding plan
---------------
- Repo layout:
  - `app.py` — Streamlit/Gradio app.
  - `src/processor.py` — parsers and summarizer wrapper.
  - `src/prompt_templates.py` — system prompt and examples.
  - `tests/` — small pytest harness for parser and prompt formatting.
  - `.env.template` — environment vars document.
- Implementation order: UI → prompt wrapper → grounding retrieval → structured output → logging → tests.

12. Test harness / evaluation plan
---------------------------------
- Unit tests for: parsing CSV/TSV, turning policy text into numbered references, and prompt/payload formatting.
- Integration test: mocked LLM responses to validate JSON schema and grounding citations.
- Manual tests: 5–10 sample policy updates (diverse short/long) run through the app and recorded in the build log.

13. Success metrics
-------------------
- Working prototype deployed at a public URL.
- Repo with at least 8–12 meaningful commits and clear README/build log entries.
- For 10 sample updates: 80% of summaries judged “accurate” by a human reviewer (basic manual rubric).
- Structured JSON returned in 95% of calls without syntax errors.

14. Risks and limitations
------------------------
- Hallucinations: LLM may invent grounding if prompts are not strict — mitigate by forcing citations.
- Privacy: uploaded policies may be sensitive — warn users and avoid sending to third-party APIs without consent.
- Dependence on paid APIs: can be mitigated using open models, but quality may vary.

15. GitHub commit plan
---------------------
- Commit 1: Repo skeleton, `roadmap.md`, `.gitignore`, `.env.template`.
- Commit 2: Basic Streamlit/Gradio UI with paste box and file upload (no LLM calls).
- Commit 3: Prompt templates and LLM wrapper (configurable to mock or real API).
- Commit 4: Grounding preprocessing and citation mechanism.
- Commit 5: Output formatting, logging, and README stub.
- Commit 6: Tests and evaluation samples.
- Commit 7: Deployment configuration and final README/build log update.

16. README/build log plan
-------------------------
- Keep a `BUILDLOG.md` or extend the main `README.md` with dated entries recording:
  - Prompt text versions and rationale.
  - Prompts tried and what changed (A/B style).
  - Test inputs and outputs with human evaluation notes.
  - Deployment URL and instructions.

17. Questions I need to answer before coding
-------------------------------------------
- Preferred UI: `Streamlit`, `Gradio`, `Flask`, or other? (Streamlit recommended for fastest path.)
- Hosting preference: Streamlit Cloud, Hugging Face Spaces, Render, or local only?
- API access: will you use a paid OpenAI API key, or prefer a free/open-model path (HF)?
- Secrets: are you comfortable using environment variables or a secrets manager? (We will never hardcode keys.)
- Sample data: what example policy/rule inputs should I include for demos? (Provide 3–5 examples if available.)
- Success definition: what human-judged threshold counts as “accurate” for summaries?

18. Step-by-step task list for building the MVP
----------------------------------------------
1. Initialize GitHub repo and push skeleton (README, `.gitignore`, `.env.template`).
2. Implement `app.py` with a textbox, file upload, example input, and submit button.
3. Add `src/prompt_templates.py` with system prompt and 2–3 few-shot examples.
4. Implement `src/processor.py` with a `prepare_grounding()` function that numbers paragraphs/rows.
5. Implement LLM wrapper in a configurable way (mock mode + real API mode using `OPENAI_API_KEY` or HF token).
6. Wire UI submit to call processor + LLM wrapper and render JSON output and pseudo-code.
7. Add a human-review warning and simple confidence heuristic (length match, presence of citations).
8. Log prompt + grounding + model output to a local `buildlog/` file.
9. Add 5 sample inputs and run manual eval; record results in `BUILDLOG.md`.
10. Add basic unit tests for parsing and prompt formatting.
11. Deploy to Streamlit Cloud or Hugging Face Spaces; add deployment steps to README.

-- Technical questions for you (please answer):
- Which UI framework do you prefer: `Streamlit`, `Gradio`, or `Flask`?
- Which hosting option do you want to target first (Streamlit Cloud, HF Spaces, Render)?
- Will you provide an API key for a paid LLM, or do you prefer a free/open-model path?
- Do you want example policy inputs included now? If so, upload 3 sample snippets or paste them here.
- What threshold should we use for “accurate” in manual evaluation (e.g., 80% of key facts present)?

-- Notes / quick-start recommendation
- For the shortest route: use `Streamlit` + OpenAI or HF Inference + Streamlit Cloud deployment. Use environment variables for keys and a mock mode for local testing without paid keys.

---
Created as a working draft to meet the course rubric — happy to iterate next on chosen UI and sample inputs.
