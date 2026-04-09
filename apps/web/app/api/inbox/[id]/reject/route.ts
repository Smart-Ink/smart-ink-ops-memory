import { NextResponse } from 'next/server';
import { prisma } from '../../../../../lib/db';

export async function POST(_: Request, { params }: { params: { id: string } }) {
  const item = await prisma.inboxItem.findUnique({ where: { id: params.id } });
  if (!item) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  if (item.status !== 'pending') return NextResponse.json({ ok: true, alreadyProcessed: true });

  await prisma.inboxItem.update({
    where: { id: item.id },
    data: { status: 'rejected', reviewedAt: new Date() },
  });

  return NextResponse.json({ ok: true });
}
