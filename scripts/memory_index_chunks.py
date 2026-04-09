#!/usr/bin/env python3
"""Index normalized chunk JSON into the memory service.

Usage:
  python scripts/memory_index_chunks.py --project-id seed-project --chunks-file scripts/sample-memory-chunks.json
"""

from __future__ import annotations

import argparse
import json
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--chunks-file", required=True)
    parser.add_argument("--memory-service-url", default="http://localhost:8102")
    args = parser.parse_args()

    with open(args.chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    payload = {"project_id": args.project_id, "chunks": chunks}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=f"{args.memory_service_url.rstrip('/')}/index",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
