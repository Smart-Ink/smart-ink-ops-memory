import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCanonicalSourceReferenceData, mapInboxCandidateToCanonical } from './inbox-review.js';

test('mapInboxCandidateToCanonical supports all required candidate types', () => {
  const cases = [
    { type: 'prompt_candidate', expected: 'Prompt' },
    { type: 'task_candidate', expected: 'Task' },
    { type: 'meeting_candidate', expected: 'Meeting' },
    { type: 'decision_candidate', expected: 'Decision' },
    { type: 'asset_candidate', expected: 'Asset' },
    { type: 'idea_candidate', expected: 'Idea' },
  ];

  for (const c of cases) {
    const out = mapInboxCandidateToCanonical({ type: c.type, title: 't', summary: 's', payload: {} });
    assert.equal(out.model, c.expected);
    assert.equal(out.data.title, 't');
  }
});

test('buildCanonicalSourceReferenceData preserves source linkage metadata', () => {
  const out = buildCanonicalSourceReferenceData(
    { id: 'in-1', projectId: 'p-1' },
    { id: 'sr-1', conversationId: 'c-1', messageId: 'm-1', chunkId: 'ch-1' },
    { canonicalType: 'Task', id: 'task-1' }
  );

  assert.equal(out.sourceType, 'canonical');
  assert.equal(out.canonicalType, 'Task');
  assert.equal(out.canonicalId, 'task-1');
  assert.equal(out.metadata.previousSourceRefId, 'sr-1');
});
