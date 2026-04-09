import { getDashboardMetrics } from '../../lib/analytics';
import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function DashboardPage() {
  const metrics = await getDashboardMetrics(DEFAULT_PROJECT_ID);
  const inbox = await prisma.inboxItem.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, take: 8, orderBy: { createdAt: 'desc' } });

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="cards">
        {Object.entries(metrics).map(([k, v]) => (
          <div key={k} className="card">
            <div style={{ fontSize: 12, textTransform: 'capitalize' }}>{k.replace(/([A-Z])/g, ' $1')}</div>
            <strong style={{ fontSize: 24 }}>{v}</strong>
          </div>
        ))}
      </div>
      <section className="section">
        <h3>Recent inbox candidates</h3>
        <table>
          <thead><tr><th>Type</th><th>Title</th><th>Status</th><th>Confidence</th></tr></thead>
          <tbody>
            {inbox.map((i) => (
              <tr key={i.id}><td>{i.type}</td><td>{i.title}</td><td>{i.status}</td><td>{i.confidenceScore.toFixed(2)}</td></tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
