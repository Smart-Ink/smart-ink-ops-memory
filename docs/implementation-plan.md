# Implementation Plan (Review Inbox Approval + Rejection + Source Linkage)

1. **Review inbox API enhancements**
   - Extend inbox API support for `approve` and `reject` actions.
   - On approval, create canonical object by inbox type and persist `SourceReference` linkage to the canonical record.
   - On rejection, update InboxItem status to `rejected` with review timestamp.

2. **Web UI updates**
   - Update inbox page to show both Approve and Reject actions for pending items.
   - Keep UX minimal while surfacing status changes immediately after action.

3. **Validation**
   - Add/extend tests for approval and rejection behavior, including canonical object creation and source reference preservation.
