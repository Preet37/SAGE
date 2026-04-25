const DB_NAME = "sage-offline";
const DB_VERSION = 1;

export interface LessonCache {
  lessonId: number;
  title: string;
  chunks: string[];
  cachedAt: number;
}

export interface OfflineMessage {
  role: "user" | "sage";
  text: string;
  timestamp: number;
}

export interface OfflineSession {
  sessionId: number;
  lessonId: number;
  messages: OfflineMessage[];
  startedAt: number;
  synced: boolean;
}

export interface MasteryQueueEntry {
  id?: number;
  type: "mastery";
  sessionId: number;
  conceptId: number;
  delta: number;
  synced: boolean;
  queuedAt: number;
}

function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = (e.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains("lesson_cache")) {
        db.createObjectStore("lesson_cache", { keyPath: "lessonId" });
      }
      if (!db.objectStoreNames.contains("offline_sessions")) {
        db.createObjectStore("offline_sessions", { keyPath: "sessionId" });
      }
      if (!db.objectStoreNames.contains("sync_queue")) {
        db.createObjectStore("sync_queue", { keyPath: "id", autoIncrement: true });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function txGet<T>(db: IDBDatabase, store: string, key: IDBValidKey): Promise<T | undefined> {
  return new Promise((resolve, reject) => {
    const req = db.transaction(store, "readonly").objectStore(store).get(key);
    req.onsuccess = () => resolve(req.result as T | undefined);
    req.onerror = () => reject(req.error);
  });
}

function txPut(db: IDBDatabase, store: string, value: unknown): Promise<void> {
  return new Promise((resolve, reject) => {
    const req = db.transaction(store, "readwrite").objectStore(store).put(value);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

function txGetAll<T>(db: IDBDatabase, store: string): Promise<T[]> {
  return new Promise((resolve, reject) => {
    const req = db.transaction(store, "readonly").objectStore(store).getAll();
    req.onsuccess = () => resolve(req.result as T[]);
    req.onerror = () => reject(req.error);
  });
}

function txAdd(db: IDBDatabase, store: string, value: unknown): Promise<void> {
  return new Promise((resolve, reject) => {
    const req = db.transaction(store, "readwrite").objectStore(store).add(value);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

let _db: IDBDatabase | null = null;

async function getDb(): Promise<IDBDatabase> {
  if (!_db) _db = await openDB();
  return _db;
}

export const lessonStore = {
  async save(cache: LessonCache): Promise<void> {
    const db = await getDb();
    await txPut(db, "lesson_cache", cache);
  },

  async get(lessonId: number): Promise<LessonCache | undefined> {
    const db = await getDb();
    return txGet<LessonCache>(db, "lesson_cache", lessonId);
  },
};

export const sessionStore = {
  async appendMessage(
    sessionId: number,
    lessonId: number,
    msg: OfflineMessage,
  ): Promise<void> {
    const db = await getDb();
    const existing = await txGet<OfflineSession>(db, "offline_sessions", sessionId);
    const session: OfflineSession = existing ?? {
      sessionId,
      lessonId,
      messages: [],
      startedAt: Date.now(),
      synced: false,
    };
    await txPut(db, "offline_sessions", { ...session, messages: [...session.messages, msg] });
  },

  async get(sessionId: number): Promise<OfflineSession | undefined> {
    const db = await getDb();
    return txGet<OfflineSession>(db, "offline_sessions", sessionId);
  },

  async getUnsynced(): Promise<OfflineSession[]> {
    const db = await getDb();
    const all = await txGetAll<OfflineSession>(db, "offline_sessions");
    return all.filter((s) => !s.synced);
  },

  async markSynced(sessionId: number): Promise<void> {
    const db = await getDb();
    const existing = await txGet<OfflineSession>(db, "offline_sessions", sessionId);
    if (existing) await txPut(db, "offline_sessions", { ...existing, synced: true });
  },
};

export const syncQueue = {
  async enqueue(entry: Omit<MasteryQueueEntry, "id">): Promise<void> {
    const db = await getDb();
    await txAdd(db, "sync_queue", entry);
  },

  async getUnsynced(): Promise<MasteryQueueEntry[]> {
    const db = await getDb();
    const all = await txGetAll<MasteryQueueEntry>(db, "sync_queue");
    return all.filter((e) => !e.synced);
  },

  async markSynced(id: number): Promise<void> {
    const db = await getDb();
    const existing = await txGet<MasteryQueueEntry>(db, "sync_queue", id);
    if (existing) await txPut(db, "sync_queue", { ...existing, synced: true });
  },
};
