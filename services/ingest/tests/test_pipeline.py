from src.chunking import chunk_message
from src.extract import extract_candidates
from src.normalize import normalize_transcript
from src.parser import ParsedConversation, ParsedMessage, parse_chatgpt_export


def test_chatgpt_export_parsing():
    payload = {
        "conversations": [
            {
                "id": "conv-1",
                "title": "Ops sync",
                "messages": [
                    {"id": "m1", "role": "user", "content": "Create prompt template"},
                    {"id": "m2", "role": "assistant", "content": "TODO: follow up with design"},
                ],
            }
        ]
    }
    parsed = parse_chatgpt_export(payload)
    assert len(parsed) == 1
    assert parsed[0].messages[0].external_id == "m1"


def test_transcript_normalization():
    conv = ParsedConversation(
        external_id="conv-1",
        title="t",
        started_at=None,
        raw_payload={},
        messages=[ParsedMessage("m1", "USER", "  Hello   world  ", None)],
    )
    normalized = normalize_transcript(conv)
    assert normalized[0]["role"] == "user"
    assert normalized[0]["content"] == "Hello world"


def test_chunking():
    text = "word " * 200
    chunks = chunk_message(text, max_chars=50)
    assert len(chunks) > 2
    assert all(len(c) <= 50 for c in chunks)


def test_inbox_candidate_creation():
    candidates = extract_candidates("Prompt template and TODO task and a meeting agenda")
    types = {c["type"] for c in candidates}
    assert "prompt_candidate" in types
    assert "task_candidate" in types
    assert "meeting_candidate" in types


def test_approval_flow_mapping_shape():
    candidate = extract_candidates("decision: use postgres")[0]
    assert candidate["type"] == "decision_candidate"
    assert "summary" in candidate
