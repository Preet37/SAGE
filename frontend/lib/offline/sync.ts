import { sessionStore, type OfflineSession } from "./store";

const DB_NAME = "sage-offline";

async function getUnsynced(): Promise<OfflineSession[]> {
  return new Promise((resolve) => {
    const req = indexedDB.open(DB_NAME);
    req.onsuccess = () => {
      const db = req.result;
      const tx = db.transaction("offline_sessions", "readonly");
      const store = tx.objectStore("offline_sessions");
      const all: OfflineSession[] = [];
      store.openCursor().onsuccess = (e) => {
        const cursor = (e.target as IDBRequest<IDBCursorWithValue | null>).result;
        if (cursor) {
          const s = cursor.value as OfflineSession;
          if (!s.synced) all.push(s);
          cursor.continue();
        } else {
          resolve(all);
        }
      };
    };
    req.onerror = () => resolve([]);
  });
}

export async function runSync(): Promise<number> {
  const unsynced = await getUnsynced();
  let count = 0;
  for (const session of unsynced) {
    await sessionStore.markSynced(session.sessionId);
    count++;
  }
  return count;
}
