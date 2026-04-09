-- Create enums
CREATE TYPE "InboxType" AS ENUM (
  'prompt_candidate',
  'task_candidate',
  'meeting_candidate',
  'decision_candidate',
  'asset_candidate',
  'idea_candidate'
);

CREATE TYPE "InboxStatus" AS ENUM ('pending', 'approved', 'rejected');

CREATE TYPE "SourceRefType" AS ENUM ('conversation', 'message', 'chunk', 'inbox_item', 'canonical');

-- Create tables
CREATE TABLE "Project" (
  "id" TEXT PRIMARY KEY,
  "name" TEXT NOT NULL,
  "description" TEXT,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP(3) NOT NULL
);

CREATE TABLE "ChatSource" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "sourceName" TEXT NOT NULL,
  "rawMetadata" JSONB,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "ChatConversation" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "chatSourceId" TEXT NOT NULL,
  "externalId" TEXT,
  "title" TEXT,
  "startedAt" TIMESTAMP(3),
  "rawPayload" JSONB NOT NULL,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "ChatMessage" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "conversationId" TEXT NOT NULL,
  "externalId" TEXT,
  "role" TEXT NOT NULL,
  "content" TEXT NOT NULL,
  "sequenceNo" INTEGER NOT NULL,
  "createdAt" TIMESTAMP(3),
  "rawPayload" JSONB
);

CREATE TABLE "ChatChunk" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "conversationId" TEXT NOT NULL,
  "messageId" TEXT NOT NULL,
  "chunkIndex" INTEGER NOT NULL,
  "content" TEXT NOT NULL,
  "tokenEstimate" INTEGER NOT NULL,
  "embeddingStatus" TEXT NOT NULL DEFAULT 'pending',
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "InboxItem" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "type" "InboxType" NOT NULL,
  "title" TEXT NOT NULL,
  "summary" TEXT NOT NULL,
  "payload" JSONB NOT NULL,
  "confidenceScore" DOUBLE PRECISION NOT NULL,
  "status" "InboxStatus" NOT NULL DEFAULT 'pending',
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "reviewedAt" TIMESTAMP(3)
);

CREATE TABLE "SourceReference" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "sourceType" "SourceRefType" NOT NULL,
  "conversationId" TEXT,
  "messageId" TEXT,
  "chunkId" TEXT,
  "inboxItemId" TEXT,
  "canonicalType" TEXT,
  "canonicalId" TEXT,
  "metadata" JSONB,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Prompt" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "body" TEXT NOT NULL,
  "tags" TEXT[] NOT NULL,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "PromptRun" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "promptId" TEXT NOT NULL,
  "runBy" TEXT,
  "input" TEXT,
  "outputSummary" TEXT,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Task" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT,
  "status" TEXT NOT NULL DEFAULT 'open',
  "owner" TEXT,
  "dueDate" TIMESTAMP(3),
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "Meeting" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "notes" TEXT,
  "meetingDate" TIMESTAMP(3),
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "MeetingDecision" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "meetingId" TEXT,
  "title" TEXT NOT NULL,
  "summary" TEXT NOT NULL,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "MeetingAction" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "meetingId" TEXT,
  "actionText" TEXT NOT NULL,
  "owner" TEXT,
  "dueDate" TIMESTAMP(3),
  "status" TEXT NOT NULL DEFAULT 'open',
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Asset" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "assetType" TEXT NOT NULL,
  "location" TEXT,
  "summary" TEXT,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "AssetUsage" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "assetId" TEXT NOT NULL,
  "context" TEXT NOT NULL,
  "usedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Idea" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "summary" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'unresolved',
  "repetitionCount" INTEGER NOT NULL DEFAULT 1,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "Decision" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "rationale" TEXT,
  "status" TEXT NOT NULL DEFAULT 'recorded',
  "decidedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sourceRefs" JSONB
);

CREATE TABLE "MemoryHit" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "queryText" TEXT NOT NULL,
  "resultChunkId" TEXT,
  "selected" BOOLEAN NOT NULL DEFAULT false,
  "metadata" JSONB,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "AnalyticsSnapshot" (
  "id" TEXT PRIMARY KEY,
  "projectId" TEXT NOT NULL,
  "snapshotDate" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "importedConversations" INTEGER NOT NULL DEFAULT 0,
  "indexedChunks" INTEGER NOT NULL DEFAULT 0,
  "pendingInbox" INTEGER NOT NULL DEFAULT 0,
  "approvedPrompts" INTEGER NOT NULL DEFAULT 0,
  "approvedTasks" INTEGER NOT NULL DEFAULT 0,
  "approvedMeetings" INTEGER NOT NULL DEFAULT 0,
  "overdueTasks" INTEGER NOT NULL DEFAULT 0,
  "repeatedUnresolvedIdeas" INTEGER NOT NULL DEFAULT 0
);

-- Indexes
CREATE INDEX "ChatConversation_projectId_chatSourceId_idx" ON "ChatConversation"("projectId", "chatSourceId");
CREATE INDEX "ChatMessage_conversationId_sequenceNo_idx" ON "ChatMessage"("conversationId", "sequenceNo");
CREATE INDEX "ChatChunk_conversationId_messageId_chunkIndex_idx" ON "ChatChunk"("conversationId", "messageId", "chunkIndex");
CREATE INDEX "InboxItem_projectId_type_status_idx" ON "InboxItem"("projectId", "type", "status");
CREATE INDEX "SourceReference_projectId_sourceType_idx" ON "SourceReference"("projectId", "sourceType");

-- Foreign keys
ALTER TABLE "ChatSource" ADD CONSTRAINT "ChatSource_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "ChatConversation" ADD CONSTRAINT "ChatConversation_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "ChatConversation" ADD CONSTRAINT "ChatConversation_chatSourceId_fkey" FOREIGN KEY ("chatSourceId") REFERENCES "ChatSource"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "ChatMessage" ADD CONSTRAINT "ChatMessage_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES "ChatConversation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "ChatChunk" ADD CONSTRAINT "ChatChunk_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES "ChatConversation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "ChatChunk" ADD CONSTRAINT "ChatChunk_messageId_fkey" FOREIGN KEY ("messageId") REFERENCES "ChatMessage"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "SourceReference" ADD CONSTRAINT "SourceReference_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES "ChatConversation"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "SourceReference" ADD CONSTRAINT "SourceReference_messageId_fkey" FOREIGN KEY ("messageId") REFERENCES "ChatMessage"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "SourceReference" ADD CONSTRAINT "SourceReference_chunkId_fkey" FOREIGN KEY ("chunkId") REFERENCES "ChatChunk"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "SourceReference" ADD CONSTRAINT "SourceReference_inboxItemId_fkey" FOREIGN KEY ("inboxItemId") REFERENCES "InboxItem"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "Prompt" ADD CONSTRAINT "Prompt_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "PromptRun" ADD CONSTRAINT "PromptRun_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Task" ADD CONSTRAINT "Task_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Meeting" ADD CONSTRAINT "Meeting_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "MeetingDecision" ADD CONSTRAINT "MeetingDecision_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "MeetingAction" ADD CONSTRAINT "MeetingAction_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Asset" ADD CONSTRAINT "Asset_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "AssetUsage" ADD CONSTRAINT "AssetUsage_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Idea" ADD CONSTRAINT "Idea_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Decision" ADD CONSTRAINT "Decision_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "MemoryHit" ADD CONSTRAINT "MemoryHit_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "AnalyticsSnapshot" ADD CONSTRAINT "AnalyticsSnapshot_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
