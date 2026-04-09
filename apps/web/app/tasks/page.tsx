import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function TasksPage() {
  const tasks = await prisma.task.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { createdAt: 'desc' } });
  return <div><h2>Tasks</h2><table><thead><tr><th>Title</th><th>Status</th><th>Owner</th><th>Due</th></tr></thead><tbody>{tasks.map((t)=><tr key={t.id}><td>{t.title}</td><td>{t.status}</td><td>{t.owner ?? '-'}</td><td>{t.dueDate?.toISOString().slice(0,10) ?? '-'}</td></tr>)}</tbody></table></div>;
}
