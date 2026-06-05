import requests


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def fetch_related_work(topic: str) -> dict:
    """
    Searches Semantic Scholar for real related research papers based on the user's topic.
    This tool allows the agent to retrieve external research context during synthesis.
    """
    topic = topic.strip()

    params = {
        "query": topic,
        "limit": 3,
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
                "query": topic,
                "source": "Semantic Scholar",
                "papers": [],
                "message": f"No related papers found for query: {topic}"
            }

        results = []

        for paper in papers:
            results.append(
                {
                    "title": paper.get("title", "Untitled"),
                    "abstract": paper.get("abstract") or "No abstract available.",
                    "year": paper.get("year"),
                    "authors": [
                        author.get("name")
                        for author in paper.get("authors", [])
                    ],
                    "url": paper.get("url")
                }
            )

        return {
            "query": topic,
            "source": "Semantic Scholar",
            "papers": results
        }

    except requests.exceptions.Timeout:
        return {
            "query": topic,
            "source": "Semantic Scholar",
            "papers": [],
            "error": "Semantic Scholar request timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "query": topic,
            "source": "Semantic Scholar",
            "papers": [],
            "error": f"Semantic Scholar request failed: {str(e)}"
        }

    except Exception as e:
        return {
            "query": topic,
            "source": "Semantic Scholar",
            "papers": [],
            "error": f"Unexpected tool error: {str(e)}"
        }