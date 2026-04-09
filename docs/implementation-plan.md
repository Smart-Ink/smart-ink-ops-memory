# Implementation Plan (Memory Adapter Interface + Search Wiring)

1. **Formalize memory adapter interface**
   - Define a clear adapter contract for memory indexing and retrieval.
   - Implement a local stub adapter that satisfies the contract for development when MemPalace runtime is unavailable.

2. **Wire memory service to interface**
   - Refactor memory service endpoints to depend on the adapter contract (not concrete internals).
   - Keep explicit TODO boundaries where actual MemPalace client calls will be injected later.

3. **Wire web memory search workflow end-to-end**
   - Ensure memory search page calls app API, which calls memory service adapter endpoint.
   - Add selection logging route/action so chosen memory hits are recorded for analytics and traceability.

4. **Validation**
   - Add/update tests for adapter behavior and run existing service tests.
