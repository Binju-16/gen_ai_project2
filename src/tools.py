import requests


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def fetch_sample_abstract(topic: str) -> dict:
    """
    Tool function used by the model to fetch a real research abstract
    from Semantic Scholar based on a topic query.
    """
    topic = topic.lower().strip()

    params = {
        "query": topic,
        "limit": 1,
        "fields": "title,abstract,year,authors,url"
    }

    try:
        response = requests.get(
            SEMANTIC_SCHOLAR_SEARCH_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        papers = data.get("data", [])

        if not papers:
            return {
                "title": "No paper found",
                "abstract": f"No Semantic Scholar paper was found for topic: {topic}",
                "source": "Semantic Scholar",
                "url": None
            }

        paper = papers[0]

        return {
            "title": paper.get("title", "Untitled"),
            "abstract": paper.get("abstract") or "No abstract available.",
            "year": paper.get("year"),
            "authors": [
                author.get("name") for author in paper.get("authors", [])
            ],
            "source": "Semantic Scholar",
            "url": paper.get("url")
        }

    except Exception as e:
        return {
            "title": "Tool error",
            "abstract": f"Semantic Scholar lookup failed: {str(e)}",
            "source": "Semantic Scholar",
            "url": None
        }