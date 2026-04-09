import { InboxStatus, InboxType, PrismaClient, SourceRefType } from '@prisma/client';

const prisma = new PrismaClient();
const projectId = 'seed-project';

async function clearProjectData() {
  await prisma.sourceReference.deleteMany({ where: { projectId } });
  await prisma.inboxItem.deleteMany({ where: { projectId } });
  await prisma.chatChunk.deleteMany({ where: { projectId } });
  await prisma.chatMessage.deleteMany({ where: { projectId } });
  await prisma.chatConversation.deleteMany({ where: { projectId } });
  await prisma.chatSource.deleteMany({ where: { projectId } });
  await prisma.promptRun.deleteMany({ where: { projectId } });
  await prisma.prompt.deleteMany({ where: { projectId } });
  await prisma.task.deleteMany({ where: { projectId } });
  await prisma.meetingDecision.deleteMany({ where: { projectId } });
  await prisma.meetingAction.deleteMany({ where: { projectId } });
  await prisma.meeting.deleteMany({ where: { projectId } });
  await prisma.assetUsage.deleteMany({ where: { projectId } });
  await prisma.asset.deleteMany({ where: { projectId } });
  await prisma.idea.deleteMany({ where: { projectId } });
  await prisma.decision.deleteMany({ where: { projectId } });
  await prisma.memoryHit.deleteMany({ where: { projectId } });
  await prisma.analyticsSnapshot.deleteMany({ where: { projectId } });
}

async function main() {
  await prisma.project.upsert({
    where: { id: projectId },
    update: {
      name: 'Smart Ink Internal Ops Memory',
      description: 'Demo seed project for ChatGPT import + review workflow'
    },
    create: {
      id: projectId,
      name: 'Smart Ink Internal Ops Memory',
      description: 'Demo seed project for ChatGPT import + review workflow'
    }
  });

  await clearProjectData();

  const chatSource = await prisma.chatSource.create({
    data: {
      projectId,
      sourceName: 'chatgpt-export',
      rawMetadata: {
        importedBy: 'ops-lead@smartink.internal',
        importedAt: '2026-04-07T14:25:00Z',
        filename: 'chatgpt_export_ops_sync_april.json'
      }
    }
  });

  const conversation = await prisma.chatConversation.create({
    data: {
      projectId,
      chatSourceId: chatSource.id,
      externalId: 'chatgpt-conv-2026-04-07-ops-sync',
      title: 'Ops sync: onboarding docs and weekly planning',
      startedAt: new Date('2026-04-07T14:00:00Z'),
      rawPayload: {
        source: 'chatgpt-export',
        participants: ['ops lead', 'assistant'],
        topic: 'ops workflow hardening'
      }
    }
  });

  const message1 = await prisma.chatMessage.create({
    data: {
      projectId,
      conversationId: conversation.id,
      externalId: 'msg-1',
      role: 'user',
      content:
        'Create a reusable weekly planning prompt template and add a follow-up task to finalize onboarding checklist by Friday.',
      sequenceNo: 0,
      createdAt: new Date('2026-04-07T14:01:00Z')
    }
  });

  const message2 = await prisma.chatMessage.create({
    data: {
      projectId,
      conversationId: conversation.id,
      externalId: 'msg-2',
      role: 'assistant',
      content:
        'Meeting agenda: review dashboard launch decision, link the onboarding guide asset, and confirm action owners.',
      sequenceNo: 1,
      createdAt: new Date('2026-04-07T14:02:00Z')
    }
  });

  const chunk1 = await prisma.chatChunk.create({
    data: {
      projectId,
      conversationId: conversation.id,
      messageId: message1.id,
      chunkIndex: 0,
      content: 'Create a reusable weekly planning prompt template.',
      tokenEstimate: 8,
      embeddingStatus: 'indexed'
    }
  });

  const chunk2 = await prisma.chatChunk.create({
    data: {
      projectId,
      conversationId: conversation.id,
      messageId: message1.id,
      chunkIndex: 1,
      content: 'Add a follow-up task to finalize onboarding checklist by Friday.',
      tokenEstimate: 11,
      embeddingStatus: 'indexed'
    }
  });

  const chunk3 = await prisma.chatChunk.create({
    data: {
      projectId,
      conversationId: conversation.id,
      messageId: message2.id,
      chunkIndex: 0,
      content: 'Meeting agenda includes dashboard launch decision and onboarding guide asset review.',
      tokenEstimate: 12,
      embeddingStatus: 'indexed'
    }
  });

  const inboxItems = await prisma.$transaction([
    prisma.inboxItem.create({
      data: {
        projectId,
        type: InboxType.prompt_candidate,
        title: 'Weekly planning prompt template',
        summary: 'Candidate reusable planning prompt identified from imported transcript.',
        payload: {
          body: 'What are the top 3 priorities, blockers, and owners for this week?'
        },
        confidenceScore: 0.89,
        status: InboxStatus.pending
      }
    }),
    prisma.inboxItem.create({
      data: {
        projectId,
        type: InboxType.task_candidate,
        title: 'Finalize onboarding checklist',
        summary: 'Follow-up task identified from user instruction in chat transcript.',
        payload: {
          owner: 'ops@smartink.internal',
          dueDate: '2026-04-11'
        },
        confidenceScore: 0.84,
        status: InboxStatus.pending
      }
    }),
    prisma.inboxItem.create({
      data: {
        projectId,
        type: InboxType.meeting_candidate,
        title: 'Dashboard launch review meeting',
        summary: 'Meeting candidate inferred from agenda language in assistant response.',
        payload: {
          meetingDate: '2026-04-12',
          notes: 'Review launch decision, assets, and action owners.'
        },
        confidenceScore: 0.8,
        status: InboxStatus.pending
      }
    })
  ]);

  await prisma.sourceReference.createMany({
    data: [
      {
        projectId,
        sourceType: SourceRefType.chunk,
        conversationId: conversation.id,
        messageId: message1.id,
        chunkId: chunk1.id,
        inboxItemId: inboxItems[0].id,
        metadata: { extractor: 'heuristic-v1', label: 'prompt' }
      },
      {
        projectId,
        sourceType: SourceRefType.chunk,
        conversationId: conversation.id,
        messageId: message1.id,
        chunkId: chunk2.id,
        inboxItemId: inboxItems[1].id,
        metadata: { extractor: 'heuristic-v1', label: 'task' }
      },
      {
        projectId,
        sourceType: SourceRefType.chunk,
        conversationId: conversation.id,
        messageId: message2.id,
        chunkId: chunk3.id,
        inboxItemId: inboxItems[2].id,
        metadata: { extractor: 'heuristic-v1', label: 'meeting' }
      }
    ]
  });

  await prisma.prompt.createMany({
    data: [
      {
        projectId,
        title: 'Weekly planning check-in',
        body: 'Summarize priorities, blockers, deadlines, and needed decisions for this week.',
        tags: ['planning', 'ops', 'weekly']
      },
      {
        projectId,
        title: 'Post-meeting action extraction',
        body: 'Extract explicit actions, owners, and due dates from this meeting transcript.',
        tags: ['meeting', 'actions', 'extraction']
      }
    ]
  });

  await prisma.task.createMany({
    data: [
      {
        projectId,
        title: 'Finalize onboarding checklist v2',
        description: 'Consolidate checklist updates from April ops sync and publish in docs.',
        status: 'open',
        owner: 'ops@smartink.internal',
        dueDate: new Date('2026-04-11T17:00:00Z')
      },
      {
        projectId,
        title: 'Validate memory search traceability',
        description: 'Ensure search results drill back to source chunk and message IDs.',
        status: 'in_progress',
        owner: 'eng@smartink.internal',
        dueDate: new Date('2026-04-15T17:00:00Z')
      }
    ]
  });

  await prisma.meeting.create({
    data: {
      projectId,
      title: 'Ops memory MVP weekly review',
      notes: 'Review import quality, inbox approvals, and overdue follow-ups.',
      meetingDate: new Date('2026-04-12T16:00:00Z')
    }
  });

  await prisma.analyticsSnapshot.create({
    data: {
      projectId,
      importedConversations: 1,
      indexedChunks: 3,
      pendingInbox: 3,
      approvedPrompts: 2,
      approvedTasks: 2,
      approvedMeetings: 1,
      overdueTasks: 1,
      repeatedUnresolvedIdeas: 0
    }
  });
}

main()
  .then(async () => prisma.$disconnect())
  .catch(async (error) => {
    console.error(error);
    await prisma.$disconnect();
    process.exit(1);
  });
