import { NextRequest, NextResponse } from 'next/server';
import { DEFAULT_PROJECT_ID, prisma } from '../../../../lib/db';

export async function POST(req: NextRequest) {
  const { query, resultId, metadata } = await req.json();

  const logged = await prisma.memoryHit.create({
    data: {
      projectId: DEFAULT_PROJECT_ID,
      queryText: String(query || ''),
      resultChunkId: String(resultId || ''),
      selected: true,
      metadata: metadata ?? {},
    },
  });

  return NextResponse.json({ ok: true, id: logged.id });
}
