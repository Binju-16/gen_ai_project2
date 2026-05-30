from src.processor import prepare_documents

def test_prepare_documents():
    docs = ["First doc.", "  ", "Second doc."]
    prepared = prepare_documents(docs)
    assert isinstance(prepared, list)
    assert prepared[0]["id"] == 0
    assert prepared[1]["id"] == 2
