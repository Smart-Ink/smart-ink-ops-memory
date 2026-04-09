import { NextResponse } from 'next/server';
import { DEFAULT_PROJECT_ID, prisma } from '../../../../../lib/db';
import { buildCanonicalSourceReferenceData, mapInboxCandidateToCanonical } from '../../../../../lib/inbox-review';

export async function POST(_: Request, { params }: { params: { id: string } }) {
  const item = await prisma.inboxItem.findUnique({ where: { id: params.id } });
  if (!item) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  if (item.status !== 'pending') return NextResponse.json({ ok: true, alreadyProcessed: true });

  const sourceRefs = await prisma.sourceReference.findMany({ where: { inboxItemId: item.id } });
  const canonicalTarget = mapInboxCandidateToCanonical(item as unknown as { type: string; title: string; summary: string; payload: Record<string, unknown>; });

  let canonical: { id: string; canonicalType: string };
  if (canonicalTarget.model === 'Prompt') {
    const record = await prisma.prompt.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Prompt' };
  } else if (canonicalTarget.model === 'Task') {
    const record = await prisma.task.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Task' };
  } else if (canonicalTarget.model === 'Meeting') {
    const record = await prisma.meeting.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Meeting' };
  } else if (canonicalTarget.model === 'Decision') {
    const record = await prisma.decision.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Decision' };
  } else if (canonicalTarget.model === 'Asset') {
    const record = await prisma.asset.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Asset' };
  } else {
    const record = await prisma.idea.create({ data: { ...canonicalTarget.data, projectId: DEFAULT_PROJECT_ID } });
    canonical = { id: record.id, canonicalType: 'Idea' };
  }

  await prisma.$transaction([
    prisma.inboxItem.update({ where: { id: item.id }, data: { status: 'approved', reviewedAt: new Date() } }),
    ...sourceRefs.map((sourceRef) =>
      prisma.sourceReference.create({
        data: buildCanonicalSourceReferenceData(item, sourceRef, canonical),
      })
    ),
  ]);

  return NextResponse.json({ ok: true, canonical });
}
