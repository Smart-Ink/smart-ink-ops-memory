# Implementation Plan (InboxItem Extraction Pipeline)

1. **Define extraction interface boundary**
   - Add a clean extractor interface that returns normalized InboxItem candidate shapes.
   - Keep deterministic heuristics as the default implementation.
   - Leave a clear extension point for future LLM-based extractor implementation.

2. **Implement deterministic heuristic extractor**
   - Build rule-based detection for prompt, task, meeting, decision, idea, and asset candidates.
   - Ensure deterministic confidence scoring and stable candidate titles/summaries/payload fields.

3. **Integrate with ingest pipeline**
   - Update `services/ingest/src/main.py` to use the extraction pipeline interface (not direct ad hoc regex calls).
   - Preserve existing chunking + persistence flow while passing extracted candidates into `InboxItem` creation.

4. **Tests**
   - Add/adjust tests verifying all required candidate types are produced and extraction remains deterministic.
