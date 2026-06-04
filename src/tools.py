SAMPLE_ABSTRACTS = {
    "education_ai": {
        "title": "AI Tutoring and Student Learning",
        "abstract": (
            "This study examines the use of AI tutoring systems in undergraduate education. "
            "Results suggest that students using AI tutors improved quiz performance, but the study also notes concerns about overreliance and unequal access."
        )
    },
    "research_synthesis": {
        "title": "Research Synthesis with Large Language Models",
        "abstract": (
            "This paper explores how large language models can support literature review workflows. "
            "The study finds that LLMs can summarize themes across papers, but human review remains necessary to verify claims and detect missing context."
        )
    },
    "healthcare_ai": {
        "title": "Machine Learning for Clinical Decision Support",
        "abstract": (
            "This study evaluates machine learning models for clinical decision support. "
            "The findings show improved prediction accuracy, but limitations include bias in training data and lack of interpretability."
        )
    }
}


def fetch_sample_abstract(topic: str) -> dict:
    """
    Tool function used by the model to fetch a built-in sample abstract.
    This demonstrates real tool/function calling for the agentic workflow.
    """
    topic = topic.lower().strip()

    if topic not in SAMPLE_ABSTRACTS:
        return {
            "title": "No sample found",
            "abstract": (
                "No built-in abstract was found for this topic. "
                "Available topics are: education_ai, research_synthesis, healthcare_ai."
            )
        }

    return SAMPLE_ABSTRACTS[topic]