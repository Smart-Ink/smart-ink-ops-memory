import { prisma } from './db';

export async function getDashboardMetrics(projectId: string) {
  const [
    importedConversations,
    indexedChunks,
    inboxPending,
    approvedPrompts,
    approvedTasks,
    approvedMeetings,
    overdueTasks,
    repeatedUnresolvedIdeas
  ] = await Promise.all([
    prisma.chatConversation.count({ where: { projectId } }),
    prisma.chatChunk.count({ where: { projectId, embeddingStatus: 'indexed' } }),
    prisma.inboxItem.count({ where: { projectId, status: 'pending' } }),
    prisma.prompt.count({ where: { projectId } }),
    prisma.task.count({ where: { projectId } }),
    prisma.meeting.count({ where: { projectId } }),
    prisma.task.count({ where: { projectId, status: 'open', dueDate: { lt: new Date() } } }),
    prisma.idea.count({ where: { projectId, status: 'unresolved', repetitionCount: { gte: 2 } } })
  ]);

  return {
    importedConversations,
    indexedChunks,
    inboxPending,
    approvedPrompts,
    approvedTasks,
    approvedMeetings,
    overdueTasks,
    repeatedUnresolvedIdeas
  };
}
