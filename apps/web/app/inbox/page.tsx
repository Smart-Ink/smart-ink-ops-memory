'use client';

import { useEffect, useState } from 'react';

type InboxItem = {
  id: string;
  type: string;
  title: string;
  summary: string;
  status: string;
  confidenceScore: number;
};

export default function InboxPage() {
  const [items, setItems] = useState<InboxItem[]>([]);

  async function load() {
    const r = await fetch('/api/inbox');
    const data = await r.json();
    setItems(data.items ?? []);
  }

  async function approve(id: string) {
    await fetch(`/api/inbox/${id}/approve`, { method: 'POST' });
    await load();
  }

  async function reject(id: string) {
    await fetch(`/api/inbox/${id}/reject`, { method: 'POST' });
    await load();
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <h2>Review Inbox</h2>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Title</th>
            <th>Summary</th>
            <th>Status</th>
            <th>Confidence</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id}>
              <td>{i.type}</td>
              <td>{i.title}</td>
              <td>{i.summary}</td>
              <td>{i.status}</td>
              <td>{i.confidenceScore.toFixed(2)}</td>
              <td>
                {i.status === 'pending' ? (
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button onClick={() => approve(i.id)}>Approve</button>
                    <button onClick={() => reject(i.id)} style={{ background: '#b91c1c' }}>
                      Reject
                    </button>
                  </div>
                ) : (
                  '-'
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
