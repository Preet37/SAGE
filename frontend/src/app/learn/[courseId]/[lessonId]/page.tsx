"use client";

import { use, useCallback, useEffect, useMemo, useRef, useState } from "react";

import AccessibilityModal from "@/components/AccessibilityModal";
import AgentPanel, {
  applyAgentEvent,
  type AgentPanelState,
} from "@/components/AgentPanel";
import AppHeader from "@/components/AppHeader";
import ConceptMap, {
  type ConceptEdge,
  type ConceptNode,
} from "@/components/ConceptMap";
import NetworkPanel from "@/components/NetworkPanel";
import NotesPanel from "@/components/NotesPanel";
import ModelDownloadBanner from "@/components/offline/ModelDownloadBanner";
import OfflineBadge from "@/components/offline/OfflineBadge";
import ProtectedRoute from "@/components/ProtectedRoute";
import ReplayPanel from "@/components/ReplayPanel";
import TutorChat, { type TutorChatHandle } from "@/components/TutorChat";
import VoiceAgent from "@/components/VoiceAgent";
import {
  bumpMastery,
  getConceptMap,
  getCourse,
  type Concept,
  type Lesson,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useConnectivity } from "@/lib/offline/connectivity";
import { splitIntoChunks } from "@/lib/offline/retriever";
import { runSync } from "@/lib/offline/sync";
import { lessonStore, syncQueue } from "@/lib/offline/store";

interface PageParams {
  courseId: string;
  lessonId: string;
}

type CenterTab = "chat" | "map" | "network" | "notes" | "replay";

export default function LearnLessonPage({ params }: { params: Promise<PageParams> }) {
  const resolved = use(params);
  return (
    <ProtectedRoute>
      <Workspace courseId={resolved.courseId} lessonId={resolved.lessonId} />
    </ProtectedRoute>
  );
}

function Workspace({ courseId, lessonId }: PageParams) {
  const { token } = useAuth();
  const sessionId = Number(lessonId) || 0;
  const courseIdNum = Number(courseId) || 0;

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [tab, setTab] = useState<CenterTab>("chat");
  const [agentState, setAgentState] = useState<AgentPanelState>({});
  const [a11yOpen, setA11yOpen] = useState(false);
  const [replayKey, setReplayKey] = useState(0);
  const [syncedCount, setSyncedCount] = useState(0);
  const chatRef = useRef<TutorChatHandle | null>(null);

  const { isOnline } = useConnectivity();
  const wasOnlineRef = useRef(isOnline);

  // Load lesson + concepts.
  useEffect(() => {
    if (!token || !courseIdNum) return;
    getCourse(courseIdNum, token).then((l) => {
      setLesson(l);
      // Pre-cache lesson chunks for offline retrieval.
      const chunks = splitIntoChunks(l.objective);
      void lessonStore.save({ lessonId: l.id, title: l.title, chunks, cachedAt: Date.now() });
    }).catch(() => setLesson(null));
  }, [courseIdNum, token]);

  const refreshConcepts = useCallback(() => {
    if (!token || !sessionId) return;
    getConceptMap(sessionId, token).then(setConcepts).catch(() => setConcepts([]));
  }, [sessionId, token]);

  useEffect(() => {
    refreshConcepts();
  }, [refreshConcepts]);

  // Auto-sync when connectivity is restored.
  useEffect(() => {
    if (isOnline && !wasOnlineRef.current && token) {
      runSync(token)
        .then(({ synced }) => {
          if (synced > 0) {
            setSyncedCount(synced);
            refreshConcepts();
            setTimeout(() => setSyncedCount(0), 4_000);
          }
        })
        .catch(() => { /* sync failures are silent; data stays queued */ });
    }
    wasOnlineRef.current = isOnline;
  }, [isOnline, token, refreshConcepts]);

  const { nodes, edges } = useMemo(() => buildGraph(concepts, lesson), [concepts, lesson]);

  const onNodeClick = useCallback(
    async (n: ConceptNode) => {
      if (!token || !n.conceptId) return;
      if (!isOnline) {
        // Queue the mastery bump for sync when back online.
        await syncQueue.enqueue({
          type: "mastery",
          sessionId,
          conceptId: n.conceptId,
          delta: 0.15,
          synced: false,
          queuedAt: Date.now(),
        });
        // Apply optimistically to local state.
        setConcepts((prev) =>
          prev.map((c) =>
            c.id === n.conceptId ? { ...c, mastery: Math.min(1, c.mastery + 0.15) } : c,
          ),
        );
        return;
      }
      try {
        const updated = await bumpMastery(sessionId, n.conceptId, 0.15, token);
        setConcepts((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
      } catch {
        /* ignore */
      }
    },
    [isOnline, sessionId, token],
  );

  if (!token) return null;

  return (
    <main className="bg-blobs flex h-screen flex-col gap-4 p-4">
      <AppHeader
        courseId={courseId}
        lessonId={lessonId}
        onOpenAccessibility={() => setA11yOpen(true)}
      />
      <AccessibilityModal token={token} open={a11yOpen} onClose={() => setA11yOpen(false)} />

      <div
        className="grid min-h-0 flex-1 gap-4"
        style={{ gridTemplateColumns: "0.85fr 1.45fr 0.95fr" }}
      >
        {/* Left: Agent panel */}
        <section className="min-h-0">
          <AgentPanel state={agentState} />
        </section>

        {/* Center: Tabs */}
        <section className="flex min-h-0 flex-col gap-2">
          <div className="flex items-center gap-2">
            <Tabs value={tab} onChange={setTab} />
            <OfflineBadge isOnline={isOnline} syncedCount={syncedCount} />
          </div>
          <div className="min-h-0 flex-1">
            {tab === "chat" && (
              <TutorChat
                ref={chatRef}
                sessionId={sessionId}
                token={token}
                lessonId={lesson?.id}
                isOnline={isOnline}
                onAgentEvent={(e) => setAgentState((prev) => applyAgentEvent(prev, e))}
                onDone={() => {
                  if (isOnline) {
                    refreshConcepts();
                    setReplayKey((k) => k + 1);
                  }
                }}
              />
            )}
            {tab === "map" && (
              <ConceptMap nodes={nodes} edges={edges} onNodeClick={onNodeClick} />
            )}
            {tab === "network" && (
              <NetworkPanel token={token} lessonId={lesson?.id ?? null} />
            )}
            {tab === "notes" && <NotesPanel sessionId={sessionId} token={token} />}
            {tab === "replay" && (
              <ReplayPanel sessionId={sessionId} token={token} refreshKey={replayKey} />
            )}
          </div>
        </section>

        {/* Right: Voice + key concepts + offline model */}
        <aside className="flex min-h-0 flex-col gap-3 overflow-y-auto pr-1">
          {isOnline && (
            <VoiceAgent
              onTranscript={(text) => {
                setTab("chat");
                chatRef.current?.submit(text);
              }}
            />
          )}
          <ModelDownloadBanner autoLoad={!isOnline} />
          <KeyConceptsCard concepts={concepts} />
          <LessonSummaryCard lesson={lesson} />
        </aside>
      </div>
    </main>
  );
}

function Tabs({ value, onChange }: { value: CenterTab; onChange: (v: CenterTab) => void }) {
  const items: { id: CenterTab; label: string }[] = [
    { id: "chat", label: "Chat" },
    { id: "map", label: "Map" },
    { id: "network", label: "Network" },
    { id: "notes", label: "Notes" },
    { id: "replay", label: "Replay" },
  ];
  return (
    <nav className="flex flex-wrap gap-1.5" aria-label="Workspace tabs">
      {items.map((it) => {
        const active = value === it.id;
        return (
          <button
            key={it.id}
            type="button"
            onClick={() => onChange(it.id)}
            className="rounded-full px-3 py-1.5 text-xs font-semibold"
            style={{
              background: active ? "var(--color-primary)" : "var(--color-muted)",
              color: active ? "var(--color-on-primary)" : "var(--color-primary)",
              border: "1px solid var(--color-border)",
              cursor: "pointer",
            }}
          >
            {it.label}
          </button>
        );
      })}
    </nav>
  );
}

function KeyConceptsCard({ concepts }: { concepts: Concept[] }) {
  if (!concepts.length) {
    return (
      <div className="card p-4">
        <p className="text-sm font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
          Key concepts
        </p>
        <p className="mt-2 text-xs opacity-60">
          Concepts will appear as you chat with SAGE.
        </p>
      </div>
    );
  }
  return (
    <div className="card p-4">
      <p className="text-sm font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
        Key concepts
      </p>
      <ul className="mt-2 space-y-1.5">
        {concepts.slice(0, 8).map((c) => (
          <li key={c.id} className="flex items-center justify-between text-xs">
            <span className="truncate">{c.label}</span>
            <span
              className="rounded-full px-2 py-0.5 font-semibold"
              style={{
                background: "var(--color-muted)",
                color:
                  c.mastery >= 0.8
                    ? "var(--color-secondary)"
                    : c.mastery >= 0.5
                      ? "var(--color-primary)"
                      : "var(--color-accent)",
              }}
            >
              {Math.round(c.mastery * 100)}%
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function LessonSummaryCard({ lesson }: { lesson: Lesson | null }) {
  if (!lesson) return null;
  return (
    <div className="card p-4">
      <p className="text-sm font-semibold" style={{ fontFamily: "var(--font-heading)" }}>
        {lesson.title}
      </p>
      <p className="mt-1 text-xs opacity-70">{lesson.subject || "General"}</p>
      <p className="mt-2 text-xs opacity-80 line-clamp-6 whitespace-pre-wrap">
        {lesson.objective || "No description provided."}
      </p>
    </div>
  );
}

function buildGraph(
  concepts: Concept[],
  lesson: Lesson | null,
): { nodes: ConceptNode[]; edges: ConceptEdge[] } {
  if (concepts.length === 0 && lesson) {
    return {
      nodes: [{ id: `lesson-${lesson.id}`, label: lesson.title, mastery: 0.1 }],
      edges: [],
    };
  }
  const nodes: ConceptNode[] = concepts.map((c) => ({
    id: `c-${c.id}`,
    label: c.label,
    mastery: c.mastery,
    conceptId: c.id,
  }));
  const edges: ConceptEdge[] = concepts
    .filter((c) => c.parent_id != null)
    .map((c) => ({ source: `c-${c.parent_id}`, target: `c-${c.id}` }));
  return { nodes, edges };
}
