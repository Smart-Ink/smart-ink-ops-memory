import { NextResponse } from 'next/server';
import { DEFAULT_PROJECT_ID, prisma } from '../../../lib/db';

export async function GET() {
  const items = await prisma.inboxItem.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { createdAt: 'desc' }, take: 200 });
  return NextResponse.json({ items });
}
