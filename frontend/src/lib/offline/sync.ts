import { bumpMastery } from "@/lib/api";

import { sessionStore, syncQueue } from "./store";

export interface SyncResult {
  synced: number;
  failed: number;
}

export async function runSync(token: string): Promise<SyncResult> {
  let synced = 0;
  let failed = 0;

  const masteryEntries = await syncQueue.getUnsynced();
  for (const entry of masteryEntries) {
    if (entry.id === undefined) continue;
    try {
      await bumpMastery(entry.sessionId, entry.conceptId, entry.delta, token);
      await syncQueue.markSynced(entry.id);
      synced++;
    } catch {
      failed++;
    }
  }

  // Offline sessions (messages) are stored locally for replay only.
  // Mark them synced so the queue stays clean — they are not replayed
  // through the backend AI pipeline since that would re-run inference.
  const offlineSessions = await sessionStore.getUnsynced();
  for (const session of offlineSessions) {
    await sessionStore.markSynced(session.sessionId);
    synced++;
  }

  return { synced, failed };
}
