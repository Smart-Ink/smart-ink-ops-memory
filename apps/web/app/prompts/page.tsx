import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function PromptsPage() {
  const prompts = await prisma.prompt.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { createdAt: 'desc' } });
  return <div><h2>Prompt Library</h2><table><thead><tr><th>Title</th><th>Body</th></tr></thead><tbody>{prompts.map((p)=><tr key={p.id}><td>{p.title}</td><td>{p.body}</td></tr>)}</tbody></table></div>;
}
