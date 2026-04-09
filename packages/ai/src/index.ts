import { ExtractedCandidate } from '@smart-ink/shared';

export function chunkText(content: string, maxLen = 600): string[] {
  if (content.length <= maxLen) return [content];
  const words = content.split(/\s+/);
  const chunks: string[] = [];
  let current = '';
  for (const word of words) {
    if ((current + ' ' + word).trim().length > maxLen) {
      chunks.push(current.trim());
      current = word;
    } else {
      current += ` ${word}`;
    }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks;
}

export function extractCandidates(content: string): ExtractedCandidate[] {
  const candidates: ExtractedCandidate[] = [];
  if (/prompt|template/i.test(content)) {
    candidates.push({
      type: 'prompt_candidate',
      title: 'Extracted prompt candidate',
      summary: 'Potential reusable prompt from transcript',
      payload: { body: content.slice(0, 300) },
      confidenceScore: 0.72,
      source: {}
    });
  }
  if (/todo|task|follow up|follow-up/i.test(content)) {
    candidates.push({
      type: 'task_candidate',
      title: 'Extracted task candidate',
      summary: 'Potential task from transcript',
      payload: { description: content.slice(0, 300) },
      confidenceScore: 0.75,
      source: {}
    });
  }
  if (/meeting|agenda/i.test(content)) {
    candidates.push({
      type: 'meeting_candidate',
      title: 'Extracted meeting candidate',
      summary: 'Potential meeting artifact from transcript',
      payload: { notes: content.slice(0, 300) },
      confidenceScore: 0.68,
      source: {}
    });
  }
  if (/decision|decide/i.test(content)) {
    candidates.push({
      type: 'decision_candidate',
      title: 'Extracted decision candidate',
      summary: 'Potential decision from transcript',
      payload: { rationale: content.slice(0, 300) },
      confidenceScore: 0.7,
      source: {}
    });
  }
  if (/asset|document|file|link/i.test(content)) {
    candidates.push({
      type: 'asset_candidate',
      title: 'Extracted asset candidate',
      summary: 'Potential asset reference from transcript',
      payload: { locationHint: content.slice(0, 200) },
      confidenceScore: 0.65,
      source: {}
    });
  }
  if (/idea|hypothesis/i.test(content)) {
    candidates.push({
      type: 'idea_candidate',
      title: 'Extracted idea candidate',
      summary: 'Potential idea from transcript',
      payload: { summary: content.slice(0, 250) },
      confidenceScore: 0.66,
      source: {}
    });
  }
  return candidates;
}
