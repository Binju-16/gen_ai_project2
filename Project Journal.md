# PROJECT JOURNAL

## Project Title

Research Synthesis Agent

---

## Project Motivation

As a graduate student in Data Science and Analytics, I regularly read research papers for coursework, projects, and independent learning. One challenge I often face is synthesizing information from multiple papers efficiently while identifying common themes, methodological differences, research gaps, and future directions.

Many AI tools can summarize a single paper, but they often fail to compare findings across multiple documents or provide structured outputs that support literature review workflows.

For Project 2, I wanted to build an agentic system that goes beyond simple summarization and acts more like a research assistant. The goal is to allow users to upload research abstracts, generate structured synthesis results, and then provide feedback that the agent can use to refine its analysis.

---

## Initial Idea

The original concept was to build a Research Synthesis Agent that could:

* Accept one or more research abstracts
* Generate a structured synthesis
* Identify major themes
* Extract methodologies
* Detect conflicting findings
* Identify research gaps
* Suggest future research questions
* Allow reviewer feedback and refinement

This project aligns with my interest in research synthesis and academic productivity.

---

## Development Process

### Version 1

The first version focused on creating a working Streamlit interface.

Implemented:

* Text input area
* File upload functionality
* Research synthesis workflow
* OpenAI integration
* Structured JSON output

At this stage, the system could generate summaries but the outputs were too generic and lacked transparency.

---

### Version 2

I improved the prompt design and added stronger output constraints.

Changes:

* Added a dedicated system prompt
* Defined a structured JSON schema
* Added grounding requirements
* Added confidence scores

Result:

Outputs became more consistent and easier to display within the application.

---

### Version 3

I introduced grounding features.

Changes:

* Source documents are stored internally
* Grounding references are returned
* Original source text is displayed to users
* Human review warning added

Result:

Users can better understand where conclusions originate and verify outputs manually.

---

### Version 4

I added the reviewer feedback loop.

Changes:

* Reviewer feedback textbox
* Feedback-based refinement workflow
* Second-pass synthesis generation

Result:

The application became more agentic because users can interact with the system and influence subsequent outputs rather than receiving a single static response.

---

## Challenges Encountered

### OpenAI API Migration

During development I encountered issues caused by changes in the OpenAI Python SDK.

The original implementation used:

openai.ChatCompletion.create()

which is no longer supported in newer SDK versions.

To resolve this issue, I migrated the application to the newer OpenAI client interface.

---

### JSON Formatting Issues

The model occasionally returned output that was not valid JSON.

To address this:

* Output constraints were strengthened
* The system prompt was updated
* Fallback parsing logic was added

---

### Grounding Visibility

Early versions only displayed grounding reference IDs such as:

[0]

This was not very informative.

I updated the interface so users can directly view the corresponding source document excerpts.

---

## Current Status

The current prototype can:

* Accept research abstracts
* Generate structured research synthesis
* Extract themes and methodologies
* Identify research gaps
* Generate future research questions
* Display source document references
* Accept reviewer feedback
* Refine outputs based on feedback
* Operate using OpenAI models through API integration

---

## Future Improvements

Planned improvements include:

1. Multi-paper comparison and synthesis
2. Better conflict detection across papers
3. Automatic citation extraction
4. PDF upload support
5. Research trend visualization
6. Literature review dashboard generation
7. Export results to Markdown or PDF

---

## Lessons Learned

This project reinforced several important concepts:

* Prompt engineering significantly affects output quality.
* Grounding is essential for trustworthy AI outputs.
* Agentic workflows benefit from user feedback loops.
* Structured outputs are easier to evaluate and refine.
* Human review remains important when working with research content.

The most valuable lesson was that creating useful AI systems requires more than connecting a model to a user interface. Careful prompt design, grounding, evaluation, and iteration are necessary to build a reliable research assistant.
