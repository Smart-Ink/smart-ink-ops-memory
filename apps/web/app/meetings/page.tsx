import { DEFAULT_PROJECT_ID, prisma } from '../../lib/db';

export default async function MeetingsPage() {
  const meetings = await prisma.meeting.findMany({ where: { projectId: DEFAULT_PROJECT_ID }, orderBy: { createdAt: 'desc' } });
  return <div><h2>Meetings</h2><table><thead><tr><th>Title</th><th>Date</th><th>Notes</th></tr></thead><tbody>{meetings.map((m)=><tr key={m.id}><td>{m.title}</td><td>{m.meetingDate?.toISOString().slice(0,10) ?? '-'}</td><td>{m.notes ?? '-'}</td></tr>)}</tbody></table></div>;
}
