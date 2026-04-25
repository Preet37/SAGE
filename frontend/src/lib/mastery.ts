"use client";

const KEY = "sage_mastered_topics";

export interface MasteredTopic {
  id: string;
  label: string;
  masteredAt: number;
}

function safeRead(): MasteredTopic[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function safeWrite(topics: MasteredTopic[]) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(KEY, JSON.stringify(topics));
    window.dispatchEvent(new CustomEvent("sage:mastery-changed"));
  } catch {
    /* ignore */
  }
}

export function slugify(label: string): string {
  return label.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "topic";
}

export function listMastered(): MasteredTopic[] {
  return safeRead();
}

export function addMastered(label: string): MasteredTopic {
  const topics = safeRead();
  const id = slugify(label);
  const existing = topics.find((t) => t.id === id);
  if (existing) return existing;
  const next: MasteredTopic = { id, label, masteredAt: Date.now() };
  safeWrite([...topics, next]);
  return next;
}

export function clearMastered() {
  safeWrite([]);
}

export function brainScale(count: number): number {
  // grow brain by ~12% every 15 mastered topics, cap at 2.0x
  return Math.min(2.0, 1 + Math.floor(count / 15) * 0.12);
}
