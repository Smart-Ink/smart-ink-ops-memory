export function mapInboxCandidateToCanonical(item) {
  const payload = item.payload || {};

  if (item.type === 'prompt_candidate') {
    return { model: 'Prompt', data: { title: item.title, body: String(payload.prompt_body || payload.body || item.summary), tags: [] } };
  }
  if (item.type === 'task_candidate') {
    return {
      model: 'Task',
      data: {
        title: item.title,
        description: String(payload.description || payload.excerpt || item.summary),
        owner: payload.owner || null,
      },
    };
  }
  if (item.type === 'meeting_candidate') {
    return { model: 'Meeting', data: { title: item.title, notes: String(payload.meeting_notes || payload.notes || item.summary) } };
  }
  if (item.type === 'decision_candidate') {
    return { model: 'Decision', data: { title: item.title, rationale: String(payload.rationale || item.summary) } };
  }
  if (item.type === 'asset_candidate') {
    return { model: 'Asset', data: { title: item.title, assetType: 'reference', summary: item.summary, location: String(payload.location_hint || payload.locationHint || '') } };
  }
  if (item.type === 'idea_candidate') {
    return { model: 'Idea', data: { title: item.title, summary: String(payload.idea_summary || payload.summary || item.summary) } };
  }
  throw new Error(`Unsupported inbox type: ${item.type}`);
}

export function buildCanonicalSourceReferenceData(item, sourceRef, canonical) {
  return {
    projectId: item.projectId,
    sourceType: 'canonical',
    conversationId: sourceRef.conversationId,
    messageId: sourceRef.messageId,
    chunkId: sourceRef.chunkId,
    inboxItemId: item.id,
    canonicalType: canonical.canonicalType,
    canonicalId: canonical.id,
    metadata: {
      approvedFromInbox: item.id,
      previousSourceRefId: sourceRef.id,
    },
  };
}
