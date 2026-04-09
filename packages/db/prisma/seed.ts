import { PrismaClient, InboxType } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const project = await prisma.project.upsert({
    where: { id: 'seed-project' },
    update: {},
    create: {
      id: 'seed-project',
      name: 'Smart Ink Internal Ops',
      description: 'Seed project for local MVP'
    }
  });

  await prisma.inboxItem.createMany({
    data: [
      {
        projectId: project.id,
        type: InboxType.prompt_candidate,
        title: 'Weekly sprint retro prompt',
        summary: 'Template for retro facilitation',
        payload: { body: 'What slowed us down this week?' },
        confidenceScore: 0.86
      },
      {
        projectId: project.id,
        type: InboxType.task_candidate,
        title: 'Publish onboarding checklist',
        summary: 'Compile onboarding process notes',
        payload: { owner: 'ops@smartink.internal' },
        confidenceScore: 0.78
      }
    ],
    skipDuplicates: true
  });
}

main()
  .then(async () => prisma.$disconnect())
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
