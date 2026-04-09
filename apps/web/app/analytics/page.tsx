import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function AnalyticsPage() {
  const snapshots = await prisma.analyticsSnapshot.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { snapshotDate: 'desc' }, take: 20 });
  return <div><h2>Basic Analytics</h2><table><thead><tr><th>Date</th><th>Imported conv</th><th>Indexed chunks</th><th>Pending inbox</th><th>Overdue tasks</th></tr></thead><tbody>{snapshots.map((s)=><tr key={s.id}><td>{s.snapshotDate.toISOString().slice(0,10)}</td><td>{s.importedConversations}</td><td>{s.indexedChunks}</td><td>{s.pendingInbox}</td><td>{s.overdueTasks}</td></tr>)}</tbody></table></div>;
}
