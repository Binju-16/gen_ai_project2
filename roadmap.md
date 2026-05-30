# Project 2 — Roadmap: Research Synthesis Agent

## 1. Project Context

The Research Synthesis Agent is an agentic AI system designed to help researchers, graduate students, and analysts quickly understand large collections of research papers. Instead of simply summarizing documents, the system performs multiple research-support tasks, including theme extraction, conflict detection, gap analysis, and future research question generation.

The project explores how generative AI can assist the literature review process by acting as an intelligent research assistant that works with user-provided research documents and continuously improves its outputs through human feedback.

This project aligns with the course focus on agentic systems by demonstrating AI that can take actions, use tools, perform multiple reasoning steps, and refine its work based on user interaction.

---

## 2. Problem Statement

Researchers often spend significant time reviewing academic papers, identifying common themes, comparing methodologies, finding conflicting findings, and discovering opportunities for future research.

Traditional AI summarization tools provide basic summaries but do not actively assist with deeper synthesis tasks.

This project aims to build an AI-powered research assistant that can:

* Analyze multiple research papers simultaneously
* Identify common themes and trends
* Detect contradictions between findings
* Discover research gaps
* Generate future research questions
* Improve results through reviewer feedback

The goal is to reduce the time required for early-stage literature reviews while keeping humans in control of the final interpretation.

---

## 3. Target User

### Primary Users

* Graduate students
* Academic researchers
* Research assistants
* Data scientists
* Faculty members

### Secondary Users

* Industry researchers
* Policy analysts
* Technical writers
* Students conducting literature reviews

---

## 4. MVP Scope for This Week

The MVP will include:

### Research Input

* Paste multiple paper abstracts
* Upload multiple text files
* Process multiple research documents simultaneously

### Agent Analysis

The system will:

* Generate structured summaries
* Extract major themes
* Identify methodologies used
* Detect possible conflicts between papers
* Identify research gaps
* Generate future research questions

### Human Feedback Loop

Users can provide feedback such as:

* Focus more on methodology
* Expand on limitations
* Generate more research questions
* Simplify explanations
* Highlight conflicting findings

The agent will revise its synthesis based on this feedback.

### Output

The system will generate:

* Research Summary
* Key Themes
* Methodologies
* Research Gaps
* Conflicting Findings
* Future Research Questions
* Confidence Score
* Human Review Warning

---

## 5. Out-of-Scope Items for the Draft

The following features are intentionally excluded from the draft version:

* Full PDF parsing
* Citation generation
* Automated paper retrieval from databases
* Vector databases
* Multi-agent orchestration frameworks
* Long-term memory
* User authentication
* Production-level security
* Fine-tuning custom models

---

## 6. Recommended Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Model

* OpenAI GPT-4o-mini

### Deployment

* Streamlit Cloud

### Environment Management

* python-dotenv

### Testing

* pytest

### Version Control

* GitHub

---

## 7. Hosting / Deployment Plan

### Development Environment

Local development will be performed using Streamlit:

```bash
streamlit run app.py
```

### Public Deployment

The application will be deployed using Streamlit Cloud.

Deployment requirements:

* Public GitHub repository
* requirements.txt
* Streamlit secrets configuration
* OpenAI API key stored securely

Deployment URL will be added to the README once available.

---

## 8. System Prompt Design

The system prompt will define the model as a Research Synthesis Agent.

### Agent Responsibilities

* Analyze uploaded research documents
* Extract major themes
* Compare findings across papers
* Identify research gaps
* Detect contradictions
* Generate future research questions
* Incorporate reviewer feedback
* Remain grounded in provided research content

### Agent Constraints

* Do not invent findings
* Do not fabricate citations
* Do not claim certainty when evidence is limited
* State uncertainty when appropriate
* Require human review for important conclusions

### Output Requirements

All responses must follow a structured schema containing:

* Summary
* Themes
* Methodologies
* Conflicts
* Research Gaps
* Future Research Questions
* Confidence Score
* Grounding References

---

## 9. Prompt Engineering Techniques

The project will demonstrate deliberate prompt engineering through:

### Role Prompting

The model will be assigned the role of an expert research synthesis assistant.

### Structured Output Prompting

The model will return information in a predefined JSON structure.

### Grounded Prompting

The model will use only uploaded documents as evidence.

### Few-Shot Prompting

Examples of desired synthesis outputs will be included.

### Constraint Prompting

Instructions will prevent unsupported conclusions and hallucinations.

### Iterative Prompt Refinement

Multiple prompt versions will be tested and documented in BUILDLOG.md.

---

## 10. Grounding Strategy

Grounding will be achieved using user-provided research content.

### Grounding Sources

* Uploaded abstracts
* Uploaded text files
* Research notes

### Grounding Rules

The model must:

* Use only provided documents
* Reference source document numbers
* Avoid unsupported claims
* Explicitly identify uncertainty

Example:

Theme: Machine Learning in Education

Supporting Sources:

* Paper 1
* Paper 3
* Paper 5

This ensures transparency and reduces hallucination risk.

---

## 11. Agent Workflow

### Step 1 — Document Collection

User uploads abstracts or research documents.

### Step 2 — Document Processing

The system:

* Cleans text
* Splits documents
* Creates document identifiers

### Step 3 — Theme Extraction

The agent identifies recurring themes across documents.

### Step 4 — Methodology Analysis

The agent identifies common research methods and approaches.

### Step 5 — Conflict Detection

The agent compares findings and highlights contradictions.

### Step 6 — Gap Analysis

The agent identifies missing research areas and unanswered questions.

### Step 7 — Research Question Generation

The agent proposes future research directions.

### Step 8 — Reviewer Feedback

The user provides feedback.

### Step 9 — Refinement

The agent updates and improves its synthesis using the feedback.

---

## 12. Test Harness / Evaluation Plan

The project will include both automated and manual evaluation.

### Evaluation Dataset

Five manually selected groups of research abstracts.

### Evaluation Criteria

#### Theme Accuracy

Did the system identify the major themes?

#### Gap Quality

Are the identified gaps meaningful?

#### Conflict Detection

Did the system identify contradictory findings?

#### Grounding

Are conclusions supported by uploaded documents?

#### Feedback Responsiveness

Did user feedback improve the synthesis?

### Manual Evaluation Rubric

Each category will be scored:

* Pass
* Partial Pass
* Fail

Results will be recorded in BUILDLOG.md.

---

## 13. Success Metrics

The project will be considered successful if:

### Functionality

* The app processes multiple documents
* The app generates a synthesis
* The app supports user feedback

### Quality

* Themes are correctly identified
* Research gaps are reasonable
* Conflicts are detected accurately

### Deployment

* Public Streamlit deployment available
* GitHub repository accessible

### Evaluation

Target:

* 80% or higher pass rate across evaluation criteria

---

## 14. Risks and Limitations

### Risks

* Hallucinated findings
* Incomplete abstracts
* Missing context
* Ambiguous research conclusions
* Limited information in short abstracts

### Mitigation Strategies

* Strong grounding instructions
* Structured prompts
* Human review warnings
* Source references
* Feedback-driven refinement

---

## 15. GitHub Commit Plan

### Commit 1

Create project structure and roadmap.

### Commit 2

Build Streamlit interface.

### Commit 3

Integrate OpenAI API.

### Commit 4

Implement document processing.

### Commit 5

Implement theme extraction.

### Commit 6

Implement conflict detection.

### Commit 7

Implement research gap analysis.

### Commit 8

Add feedback refinement loop.

### Commit 9

Add evaluation framework.

### Commit 10

Deploy application and update documentation.

---

## 16. README / Build Log Plan

### README

The README will include:

* Project overview
* Motivation
* Features
* Technology stack
* Deployment URL
* Installation instructions
* Example inputs and outputs
* Evaluation methodology

### BUILDLOG

BUILDLOG.md will document:

* Prompt iterations
* Prompt engineering decisions
* Testing results
* Failures and fixes
* Evaluation outcomes
* Lessons learned

---

## 17. Questions to Answer Before Final Submission

### Research Questions

* How many papers should be analyzed simultaneously?
* What defines a meaningful research gap?
* How should conflicts be identified?

### System Questions

* How should feedback modify outputs?
* What confidence metrics should be reported?
* What evaluation criteria matter most?

### User Experience Questions

* How much detail should summaries contain?
* How should findings be visualized?
* What information is most valuable to researchers?

---

## 18. Step-by-Step Task List for Building the MVP

### Phase 1 — Foundation

* Create repository
* Configure Streamlit
* Configure OpenAI API
* Build user interface

### Phase 2 — Core Agent

* Implement document ingestion
* Implement synthesis generation
* Implement theme extraction
* Implement methodology analysis

### Phase 3 — Advanced Analysis

* Implement conflict detection
* Implement research gap identification
* Implement research question generation

### Phase 4 — Feedback Loop

* Implement reviewer feedback input
* Implement synthesis refinement
* Compare original and revised outputs

### Phase 5 — Evaluation

* Create evaluation dataset
* Develop scoring rubric
* Run test cases
* Record results

### Phase 6 — Deployment

* Deploy to Streamlit Cloud
* Verify functionality
* Update README
* Finalize BUILDLOG

---

## Project Vision

The Research Synthesis Agent aims to become an intelligent literature review assistant capable of helping researchers understand large collections of research papers, identify knowledge gaps, compare findings, and generate future research directions through an interactive, grounded, and feedback-driven workflow.
