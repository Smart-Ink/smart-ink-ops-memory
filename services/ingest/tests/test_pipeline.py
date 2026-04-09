from src.chunking import build_exchange_pairs, chunk_exchange_pairs
from src.extract import extract_candidates
from src.normalize import normalize_transcript
from src.parser import ParsedConversation, ParsedMessage, parse_chatgpt_export


def test_chatgpt_export_parsing_mapping_style():
    payload = {
        "conversations": [
            {
                "id": "conv-1",
                "title": "Ops sync",
                "mapping": {
                    "n1": {
                        "id": "n1",
                        "message": {
                            "id": "m1",
                            "author": {"role": "user"},
                            "content": {"parts": ["Create prompt template"]},
                            "create_time": 1712496000,
                        },
                    },
                    "n2": {
                        "id": "n2",
                        "message": {
                            "id": "m2",
                            "author": {"role": "assistant"},
                            "content": {"parts": ["TODO: follow up with design"]},
                            "create_time": 1712496010,
                        },
                    },
                },
            }
        ]
    }
    parsed = parse_chatgpt_export(payload)
    assert len(parsed) == 1
    assert [m.external_id for m in parsed[0].messages] == ["m1", "m2"]


def test_transcript_normalization_order_and_cleanup():
    conv = ParsedConversation(
        external_id="conv-1",
        title="t",
        started_at=None,
        raw_payload={},
        messages=[
            ParsedMessage("m1", "USER", "  Hello   world  ", None),
            ParsedMessage("m2", "assistant", " Sure,   done ", None),
        ],
    )
    normalized = normalize_transcript(conv)
    assert normalized[0]["role"] == "user"
    assert normalized[0]["content"] == "Hello world"
    assert normalized[1]["sequence_no"] == 1


def test_chunking_by_exchange_pairs():
    normalized_messages = [
        {"external_id": "m1", "role": "user", "content": "Question about prompt", "sequence_no": 0, "created_at": None},
        {"external_id": "m2", "role": "assistant", "content": "Answer with template", "sequence_no": 1, "created_at": None},
        {"external_id": "m3", "role": "user", "content": "Follow-up task", "sequence_no": 2, "created_at": None},
    ]
    pairs = build_exchange_pairs(normalized_messages)
    assert len(pairs) == 2
    assert pairs[0]["message_external_ids"] == ["m1", "m2"]

    chunks = chunk_exchange_pairs(pairs, max_chars=40)
    assert len(chunks) >= 2
    assert all("message_external_ids" in c for c in chunks)


def test_inbox_candidate_creation_from_pair_text():
    pair_text = "User: Prompt template and TODO task\nAssistant: Meeting agenda"
    candidates = extract_candidates(pair_text)
    types = {c["type"] for c in candidates}
    assert "prompt_candidate" in types
    assert "task_candidate" in types
    assert "meeting_candidate" in types


def test_approval_flow_mapping_shape():
    candidate = extract_candidates("decision: use postgres")[0]
    assert candidate["type"] == "decision_candidate"
    assert "summary" in candidate
