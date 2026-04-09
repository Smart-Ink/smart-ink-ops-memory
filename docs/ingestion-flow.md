# Ingestion Flow

1. Client uploads ChatGPT export JSON through `POST /api/import` in web app.
2. Web app forwards payload to ingest service (`/import/chatgpt`).
3. Ingest service:
   - validates and parses conversations
   - normalizes each message
   - chunks transcript text
   - persists `ChatSource`, `ChatConversation`, `ChatMessage`, `ChatChunk`
   - creates extraction candidates in `InboxItem`
   - writes `SourceReference` rows back to chat objects
4. Ingest service sends normalized chunks to memory service indexing endpoint.
5. Memory service calls adapter `index_conversation_chunks(...)`.
6. Web dashboard + inbox reflect ingested and extracted records.
