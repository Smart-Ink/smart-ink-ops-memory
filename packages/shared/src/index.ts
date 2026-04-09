export const inboxTypes = [
  'prompt_candidate',
  'task_candidate',
  'meeting_candidate',
  'decision_candidate',
  'asset_candidate',
  'idea_candidate'
] as const;

export type InboxType = (typeof inboxTypes)[number];

export const inboxStatuses = ['pending', 'approved', 'rejected'] as const;
export type InboxStatus = (typeof inboxStatuses)[number];

export interface SourceTrace {
  conversationId?: string;
  messageId?: string;
  chunkId?: string;
}

export interface ExtractedCandidate {
  type: InboxType;
  title: string;
  summary: string;
  payload: Record<string, unknown>;
  confidenceScore: number;
  source: SourceTrace;
}
