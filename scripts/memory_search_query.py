#!/usr/bin/env python3
"""Run a memory search query against the memory service.

Usage:
  python scripts/memory_search_query.py --project-id seed-project --query "onboarding checklist"
"""

from __future__ import annotations

import argparse
import json
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--memory-service-url", default="http://localhost:8102")
    args = parser.parse_args()

    payload = {"project_id": args.project_id, "query": args.query, "limit": args.limit}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=f"{args.memory_service_url.rstrip('/')}/search",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
