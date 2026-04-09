'use client';

import { useState } from 'react';

type Result = { id: string; score: number; snippet: string; metadata: Record<string, string> };

export default function MemoryPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Result[]>([]);

  async function onSearch() {
    const r = await fetch('/api/memory/search', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ query }) });
    const data = await r.json();
    setResults(data.results ?? []);
  }

  return (
    <div>
      <h2>Memory Search</h2>
      <div className="section" style={{ display: 'flex', gap: 8 }}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search memory" style={{ width: 420 }} />
        <button onClick={onSearch}>Search</button>
      </div>
      <table>
        <thead><tr><th>Score</th><th>Snippet</th><th>Source metadata</th></tr></thead>
        <tbody>
          {results.map((item) => (
            <tr key={item.id}><td>{item.score.toFixed(2)}</td><td>{item.snippet}</td><td>{JSON.stringify(item.metadata)}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
