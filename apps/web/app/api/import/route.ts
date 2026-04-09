import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const payload = await req.json();
  const ingestBase = process.env.INGEST_SERVICE_URL || 'http://localhost:8101';
  const response = await fetch(`${ingestBase}/import/chatgpt`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
