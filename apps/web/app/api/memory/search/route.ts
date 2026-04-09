import { NextRequest, NextResponse } from 'next/server';
import { DEFAULT_PROJECT_ID, prisma } from '../../../../lib/db';

export async function POST(req: NextRequest) {
  const { query, limit = 10 } = await req.json();
  const memoryBase = process.env.MEMORY_SERVICE_URL || 'http://localhost:8102';
  const response = await fetch(`${memoryBase}/search`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ query, project_id: DEFAULT_PROJECT_ID, limit })
  });
  const data = await response.json();

  await prisma.memoryHit.create({
    data: {
      projectId: DEFAULT_PROJECT_ID,
      queryText: query,
      metadata: { resultCount: data.results?.length ?? 0 }
    }
  });

  return NextResponse.json(data, { status: response.status });
}
