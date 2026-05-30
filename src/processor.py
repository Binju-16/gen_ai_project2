from typing import List

def prepare_documents(docs: List[str]):
    """Simple preprocessing: trim and index documents."""
    prepared = []
    for i, d in enumerate(docs):
        text = d.strip()
        if not text:
            continue
        prepared.append({"id": i, "text": text})
    return prepared
