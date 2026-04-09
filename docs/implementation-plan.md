# Implementation Plan (MemPalace Adapter Integration + Memory CLI Scripts)

1. **Add real MemPalace adapter implementation**
   - Implement a production adapter that calls MemPalace HTTP endpoints for indexing/search.
   - Keep the existing local stub adapter for local development fallback.

2. **Adapter selection + wiring**
   - Update adapter factory and memory service startup to support `MEMORY_ADAPTER_MODE=stub|mempalace`.
   - Validate required MemPalace environment variables when `mempalace` mode is selected.

3. **Add executable scripts/commands**
   - Add scripts to index normalized chunks and run search queries against the memory service.
   - Document usage in README/docs with concrete command examples.

4. **Validation**
   - Add adapter tests for MemPalace HTTP mode (mocked HTTP client) and run existing test suites.
