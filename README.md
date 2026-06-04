# Research Synthesis Agent

## Live Application
https://genaiproject2-7wki78ter6y2rdjtb89jji.streamlit.app/

## Overview

Research Synthesis Agent is an AI-powered research assistant built using Streamlit and OpenAI. The system helps users analyze research abstracts and research documents by generating structured literature-review style outputs.

Unlike a traditional summarization tool, the agent performs multiple research-support tasks, including:

* Research synthesis
* Theme extraction
* Methodology identification
* Research gap analysis
* Future research question generation
* Reviewer-feedback refinement

The project was developed for Project 2 (Agentic Systems) in the Generative AI course.

---

## Motivation

As a graduate student in Data Science and Analytics, I frequently read research papers for coursework, projects, and professional development. One challenge is quickly understanding multiple papers while identifying common themes, limitations, and future opportunities.

This project explores how AI can assist researchers during the literature review process while keeping humans in control of final decisions.

---

## Agent Workflow

The Research Synthesis Agent performs the following workflow:

### Step 1: Collect Documents

The user provides:

* Research abstracts
* Research notes
* Text documents

### Step 2: Analyze Research Content

The agent reviews the uploaded content and extracts:

* Major findings
* Key themes
* Research methodologies

### Step 3: Generate Research Synthesis

The agent creates a structured synthesis containing:

* Research Summary
* Major Themes
* Methodologies
* Conflicting Findings
* Research Gaps
* Future Research Questions

### Step 4: Ground Outputs

The agent references the uploaded source documents and displays grounding information.

### Step 5: Accept Reviewer Feedback

The user can provide feedback such as:

* Focus more on methodology
* Expand limitations
* Generate stronger research questions

### Step 6: Refine Output

The agent revises its synthesis based on the reviewer feedback.

---

## Features

### Research Analysis

* Structured research summaries
* Theme extraction
* Methodology extraction
* Research gap detection
* Future research question generation

### Grounding

* Source document display
* Grounding references
* Human-review warning

### Agentic Behavior

* Multi-step workflow
* Feedback-driven refinement
* Iterative synthesis generation

---

### Tool Calling

The Research Synthesis Agent uses OpenAI function calling to support agentic behavior.

Available Tool:

#### fetch_sample_abstract(topic)

Purpose:

Retrieve a sample research abstract when insufficient research content is available.

Agent Workflow:

1. User submits a request
2. Model evaluates available information
3. Model decides whether a tool is required
4. Tool executes
5. Tool returns research content
6. Model generates a grounded synthesis

Example:

No research document provided

↓

Model calls fetch_sample_abstract()

↓

Tool returns sample abstract

↓

Model generates research synthesis

This functionality was added after instructor feedback identified that the initial draft relied solely on prompting rather than true tool use.

## Example Output

The agent generates outputs in the following structure:

```json
{
  "research_summary": "...",
  "major_themes": [],
  "methodologies": [],
  "conflicting_findings": [],
  "research_gaps": [],
  "future_research_questions": [],
  "confidence_score": 0.95,
  "grounding_refs": []
}
```

---

## Prompt Engineering

The project uses several prompt-engineering techniques:

### Role Prompting

The model is instructed to behave as a Research Synthesis Agent.

### Structured Output Prompting

The model must return valid JSON following a predefined schema.

### Grounded Prompting

The model is instructed to use only uploaded research documents.

### Constraint Prompting

The model is prohibited from fabricating citations or unsupported findings.

### Iterative Refinement

The system accepts reviewer feedback and generates improved outputs.

Prompt iterations and design decisions are documented in BUILDLOG.md.

---

## Grounding Strategy

The system is grounded using user-provided research content.

Grounding sources include:

* Research abstracts
* Text documents
* Research notes

The application displays:

* Source document previews
* Grounding references
* Human review warnings

This helps users verify where conclusions originate.

---

## Evaluation

The system is evaluated using multiple research-paper test cases.

Evaluation criteria include:

* Summary quality
* Theme extraction quality
* Methodology identification
* Research gap quality
* Conflict detection
* Grounding accuracy
* Feedback responsiveness

Detailed results are documented in EVALUATION.md.

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Model

* OpenAI GPT-4o-mini

### Deployment

* Streamlit Community Cloud

### Supporting Libraries

* openai
* python-dotenv
* pytest

---

## Local Installation

Clone the repository:

```bash
git clone <repository-url>
cd gen_ai_project2
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
MOCK_MODE=0
```

Run the application:

```bash
streamlit run app.py
```

---

## Project Documentation

Additional project documentation:

* roadmap.md
* PROJECT_JOURNAL.md
* BUILDLOG.md
* EVALUATION.md

These documents describe the project's planning, development process, testing, prompt engineering decisions, and evaluation results.

---

## Human Review Warning

This application is intended to assist research synthesis and literature review.
Generated outputs should be reviewed by a human before being used in academic, professional, or research decision-making.
