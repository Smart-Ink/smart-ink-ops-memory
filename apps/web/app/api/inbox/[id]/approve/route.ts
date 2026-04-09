import { NextResponse } from 'next/server';
import { DEFAULT_PROJECT_ID, prisma } from '../../../../../lib/db';

export async function POST(_: Request, { params }: { params: { id: string } }) {
  const item = await prisma.inboxItem.findUnique({ where: { id: params.id } });
  if (!item) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  if (item.status !== 'pending') return NextResponse.json({ ok: true, alreadyProcessed: true });

  const payload = (item.payload || {}) as Record<string, unknown>;

  if (item.type === 'prompt_candidate') {
    await prisma.prompt.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, body: String(payload.body || item.summary), tags: [] } });
  } else if (item.type === 'task_candidate') {
    await prisma.task.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, description: String(payload.description || item.summary), owner: (payload.owner as string | undefined) ?? null } });
  } else if (item.type === 'meeting_candidate') {
    await prisma.meeting.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, notes: String(payload.notes || item.summary) } });
  } else if (item.type === 'decision_candidate') {
    await prisma.decision.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, rationale: String(payload.rationale || item.summary) } });
  } else if (item.type === 'asset_candidate') {
    await prisma.asset.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, assetType: 'reference', summary: item.summary, location: String(payload.locationHint || '') } });
  } else if (item.type === 'idea_candidate') {
    await prisma.idea.create({ data: { projectId: DEFAULT_PROJECT_ID, title: item.title, summary: String(payload.summary || item.summary) } });
  }

  await prisma.inboxItem.update({ where: { id: item.id }, data: { status: 'approved', reviewedAt: new Date() } });

  return NextResponse.json({ ok: true });
}
