from __future__ import annotations

from typing import Any


def extract_candidates(text: str) -> list[dict[str, Any]]:
    checks = [
        ("prompt_candidate", ["prompt", "template"], "Prompt candidate"),
        ("task_candidate", ["todo", "task", "follow up"], "Task candidate"),
        ("meeting_candidate", ["meeting", "agenda"], "Meeting candidate"),
        ("decision_candidate", ["decision", "decide"], "Decision candidate"),
        ("asset_candidate", ["asset", "doc", "file", "link"], "Asset candidate"),
        ("idea_candidate", ["idea", "hypothesis"], "Idea candidate"),
    ]
    lowered = text.lower()
    out: list[dict[str, Any]] = []
    for item_type, keywords, title_prefix in checks:
        if any(k in lowered for k in keywords):
            out.append(
                {
                    "type": item_type,
                    "title": title_prefix,
                    "summary": text[:180],
                    "payload": {"excerpt": text[:320]},
                    "confidence_score": 0.7,
                }
            )
    return out
