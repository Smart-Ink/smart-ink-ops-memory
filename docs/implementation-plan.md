# Implementation Plan (ChatGPT Conversations Import Upgrade)

1. **Parser upgrade for conversations-style exports**
   - Implement robust parsing for ChatGPT export JSON that supports conversation records with `mapping` nodes and legacy `messages` arrays.
   - Normalize into ordered conversation/message objects with stable IDs, roles, timestamps, and cleaned content.

2. **Exchange-pair chunking**
   - Add chunking logic that groups transcript text by user/assistant exchange pairs (instead of per-message chunks).
   - Keep chunk metadata linking each chunk to source message IDs used in the pair.

3. **Persistence pipeline integration**
   - Wire parser + normalization + exchange-pair chunking through `services/ingest/src/main.py`.
   - Persist conversations/messages/chunks/candidates/source references in Postgres and keep app API import route behavior intact.

4. **Tests**
   - Expand ingestion tests to cover conversations-style mapping parsing, normalization order, exchange-pair chunking, and pipeline candidate generation assumptions.
