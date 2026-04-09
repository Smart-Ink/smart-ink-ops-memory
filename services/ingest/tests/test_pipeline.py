from src.chunking import build_exchange_pairs, chunk_exchange_pairs
from src.extract import (
    DeterministicHeuristicExtractor,
    ExtractionInput,
    extract_candidates,
    get_extractor,
)
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


def test_deterministic_extractor_generates_all_required_candidate_types():
    text = (
        "Prompt template for onboarding. TODO task owner assigned. "
        "Meeting agenda for weekly sync. Decision approved by team. "
        "Idea hypothesis for experiment. Link to asset document in Notion."
    )
    candidates = extract_candidates(text, conversation_external_id="conv-1", message_external_ids=["m1", "m2"])
    types = {c["type"] for c in candidates}

    assert {
        "prompt_candidate",
        "task_candidate",
        "meeting_candidate",
        "decision_candidate",
        "idea_candidate",
        "asset_candidate",
    }.issubset(types)


def test_extraction_interface_is_deterministic_and_has_llm_boundary():
    extractor = get_extractor("deterministic")
    assert isinstance(extractor, DeterministicHeuristicExtractor)

    extraction_input = ExtractionInput(text="Decision approved. TODO task.", conversation_external_id="conv-x")
    first = extractor.extract(extraction_input)
    second = extractor.extract(extraction_input)
    assert first == second

    try:
        get_extractor("llm").extract(extraction_input)
        assert False, "LLM extractor should not be enabled in scaffold"
    except NotImplementedError:
        assert True
