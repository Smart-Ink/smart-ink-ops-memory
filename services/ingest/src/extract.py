from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol


CandidateDict = dict[str, Any]


@dataclass(frozen=True)
class ExtractionInput:
    text: str
    conversation_external_id: str | None = None
    message_external_ids: list[str] | None = None


class CandidateExtractor(Protocol):
    def extract(self, extraction_input: ExtractionInput) -> list[CandidateDict]:
        ...


@dataclass(frozen=True)
class RuleSpec:
    candidate_type: str
    title: str
    keywords: tuple[str, ...]
    base_confidence: float


class DeterministicHeuristicExtractor:
    """Deterministic, rule-based extractor used for MVP.

    This class is intentionally stateless and deterministic to keep review workflows predictable.
    """

    RULES: tuple[RuleSpec, ...] = (
        RuleSpec("prompt_candidate", "Prompt candidate", ("prompt", "template", "instruction"), 0.74),
        RuleSpec("task_candidate", "Task candidate", ("todo", "task", "follow up", "action item", "owner"), 0.76),
        RuleSpec("meeting_candidate", "Meeting candidate", ("meeting", "agenda", "sync", "standup"), 0.72),
        RuleSpec("decision_candidate", "Decision candidate", ("decision", "decide", "approved", "chose"), 0.78),
        RuleSpec("idea_candidate", "Idea candidate", ("idea", "hypothesis", "experiment", "proposal"), 0.7),
        RuleSpec("asset_candidate", "Asset candidate", ("asset", "document", "doc", "file", "link", "notion"), 0.68),
    )

    def extract(self, extraction_input: ExtractionInput) -> list[CandidateDict]:
        lowered = extraction_input.text.lower()
        normalized = " ".join(extraction_input.text.split())
        candidates: list[CandidateDict] = []

        for rule in self.RULES:
            matches = [keyword for keyword in rule.keywords if keyword in lowered]
            if not matches:
                continue

            confidence = min(0.95, rule.base_confidence + (len(matches) - 1) * 0.03)
            candidates.append(
                {
                    "type": rule.candidate_type,
                    "title": self._build_title(rule, normalized),
                    "summary": normalized[:220],
                    "payload": self._build_payload(rule.candidate_type, normalized, matches, extraction_input),
                    "confidence_score": round(confidence, 2),
                }
            )

        return candidates

    @staticmethod
    def _build_title(rule: RuleSpec, text: str) -> str:
        sentence = re.split(r"[.!?]", text)[0].strip()
        short = sentence[:72] + ("..." if len(sentence) > 72 else "")
        return f"{rule.title}: {short}" if short else rule.title

    @staticmethod
    def _build_payload(candidate_type: str, text: str, matches: list[str], extraction_input: ExtractionInput) -> CandidateDict:
        base_payload: CandidateDict = {
            "excerpt": text[:360],
            "matched_keywords": matches,
            "conversation_external_id": extraction_input.conversation_external_id,
            "message_external_ids": extraction_input.message_external_ids or [],
            "extractor": "deterministic-heuristic-v1",
        }

        if candidate_type == "prompt_candidate":
            base_payload["prompt_body"] = text[:500]
        elif candidate_type == "task_candidate":
            base_payload["suggested_status"] = "open"
        elif candidate_type == "meeting_candidate":
            base_payload["meeting_notes"] = text[:500]
        elif candidate_type == "decision_candidate":
            base_payload["rationale"] = text[:500]
        elif candidate_type == "idea_candidate":
            base_payload["idea_summary"] = text[:500]
        elif candidate_type == "asset_candidate":
            base_payload["location_hint"] = text[:240]

        return base_payload


class LLMCandidateExtractor:
    """Placeholder extractor boundary for future model-based extraction.

    TODO(environment-specific): implement LLM invocation, prompting, and output validation.
    """

    def extract(self, extraction_input: ExtractionInput) -> list[CandidateDict]:
        raise NotImplementedError("LLMCandidateExtractor is not enabled in this scaffold.")


def get_extractor(mode: str = "deterministic") -> CandidateExtractor:
    if mode == "deterministic":
        return DeterministicHeuristicExtractor()
    if mode == "llm":
        return LLMCandidateExtractor()
    raise ValueError(f"Unknown extractor mode: {mode}")


def extract_candidates(
    text: str,
    conversation_external_id: str | None = None,
    message_external_ids: list[str] | None = None,
    mode: str = "deterministic",
) -> list[CandidateDict]:
    extractor = get_extractor(mode)
    return extractor.extract(
        ExtractionInput(
            text=text,
            conversation_external_id=conversation_external_id,
            message_external_ids=message_external_ids,
        )
    )
