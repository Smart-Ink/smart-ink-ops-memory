import { PrismaClient } from '@prisma/client';

declare global {
  // eslint-disable-next-line no-var
  var __smartInkPrisma: PrismaClient | undefined;
}

export const prisma = global.__smartInkPrisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  global.__smartInkPrisma = prisma;
}

export * from '@prisma/client';
