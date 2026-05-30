# Research Synthesis Agent — Project 2 Draft

This project is an agentic AI research assistant built with Streamlit and OpenAI. It helps users synthesize multiple research abstracts or text documents by identifying key themes, methodologies, conflicts, research gaps, and future research questions.

## Project Goal

The goal is to build a working draft of an AI system that goes beyond simple summarization. The agent analyzes user-provided research content, produces a structured synthesis, accepts reviewer feedback, and refines its output.

## Features

- Paste multiple paper abstracts
- Upload multiple text files
- Generate structured research synthesis
- Extract major themes
- Identify methodologies
- Detect possible conflicts
- Suggest research gaps
- Generate future research questions
- Refine output using user feedback
- Include human review warning

## Tech Stack

- Python
- Streamlit
- OpenAI API
- python-dotenv
- pytest
- Streamlit Cloud

## How It Is Agentic

The system performs a multi-step workflow:

1. Collects research documents
2. Processes uploaded content
3. Synthesizes findings
4. Identifies themes and gaps
5. Detects possible conflicts
6. Asks for user feedback
7. Revises the synthesis based on feedback

## Grounding Strategy

The model is grounded in the research text provided by the user. It is instructed not to invent findings or make unsupported claims. Outputs should reference the uploaded documents whenever possible.

## Prompt Engineering

This project uses:

- Role prompting
- Structured JSON output
- Grounding constraints
- Few-shot examples
- Reviewer feedback refinement
- Human review warning

Prompt iterations and testing notes are documented in `BUILDLOG.md`.

