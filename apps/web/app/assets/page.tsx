import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function AssetsPage() {
  const assets = await prisma.asset.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { createdAt: 'desc' } });
  return <div><h2>Assets</h2><table><thead><tr><th>Title</th><th>Type</th><th>Location</th></tr></thead><tbody>{assets.map((a)=><tr key={a.id}><td>{a.title}</td><td>{a.assetType}</td><td>{a.location ?? '-'}</td></tr>)}</tbody></table></div>;
}
