# Review Queue

All extracted items are first-class review candidates in `InboxItem`.

## Inbox statuses
- `pending`
- `approved`
- `rejected`

## Approval flow
1. Reviewer opens Inbox module.
2. Reviewer inspects candidate payload + source references.
3. Reviewer approves item from `POST /api/inbox/:id/approve`.
4. Backend maps inbox type to canonical table:
   - `prompt_candidate` -> `Prompt`
   - `task_candidate` -> `Task`
   - `meeting_candidate` -> `Meeting`
   - `decision_candidate` -> `Decision`
   - `asset_candidate` -> `Asset`
   - `idea_candidate` -> `Idea`
5. Item status is updated to `approved`, source traceability remains linked.
