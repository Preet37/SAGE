"use client";

import { useMemo } from "react";

import AppHeader from "@/components/AppHeader";
import ConceptMap, { ConceptEdge, ConceptNode } from "@/components/ConceptMap";
import TutorChat from "@/components/TutorChat";
import ZeticAgent from "@/components/ZeticAgent";

interface PageParams {
  courseId: string;
  lessonId: string;
}

export default function LearnPage({ params }: { params: PageParams }) {
  const sessionId = useMemo(() => Number(params.lessonId) || 1, [params.lessonId]);
  const token = typeof window !== "undefined" ? localStorage.getItem("sage_token") ?? "" : "";

  // Demo data — wire to /concept-map/{session_id} once a session exists.
  const nodes: ConceptNode[] = [
    { id: "photosynthesis", label: "Photosynthesis", mastery: 0.4 },
    { id: "chlorophyll",    label: "Chlorophyll",    mastery: 0.7 },
    { id: "light",          label: "Light",          mastery: 0.9 },
    { id: "atp",            label: "ATP",            mastery: 0.2 },
    { id: "stomata",        label: "Stomata",        mastery: 0.55 },
  ];
  const edges: ConceptEdge[] = [
    { source: "photosynthesis", target: "chlorophyll" },
    { source: "photosynthesis", target: "light" },
    { source: "photosynthesis", target: "atp" },
    { source: "photosynthesis", target: "stomata" },
  ];

  return (
    <main className="bg-blobs flex h-screen flex-col gap-4 p-4">
      <AppHeader courseId={params.courseId} lessonId={params.lessonId} />
      <div
        className="grid min-h-0 flex-1 gap-4"
        style={{ gridTemplateColumns: "1.1fr 1.3fr 1fr" }}
      >
        <section className="min-h-0">
          <TutorChat sessionId={sessionId} token={token} />
        </section>

        <section className="min-h-0">
          <ConceptMap nodes={nodes} edges={edges} />
        </section>

        <aside className="flex min-h-0 flex-col gap-4">
          <NotesPanel courseId={params.courseId} lessonId={params.lessonId} />
          <ZeticAgent />
        </aside>
      </div>
    </main>
  );
}

function NotesPanel({ courseId, lessonId }: PageParams) {
  return (
    <div className="card flex-1 overflow-auto p-5">
      <div className="flex items-center justify-between">
        <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>
          Notes
        </h2>
        <button
          className="rounded-full px-3 py-1 text-xs font-semibold"
          style={{
            background: "var(--color-muted)",
            color: "var(--color-primary)",
            border: "1px solid var(--color-border)",
            cursor: "pointer",
          }}
        >
          Export
        </button>
      </div>
      <p className="mt-2 text-sm opacity-70">
        Course <span className="font-semibold">{courseId}</span> · Lesson{" "}
        <span className="font-semibold">{lessonId}</span>
      </p>
      <div className="mt-4 space-y-2">
        <div
          className="h-3 w-5/6 rounded-full shimmer"
          style={{ background: "var(--color-muted)" }}
        />
        <div
          className="h-3 w-3/4 rounded-full shimmer"
          style={{ background: "var(--color-muted)" }}
        />
        <div
          className="h-3 w-2/3 rounded-full shimmer"
          style={{ background: "var(--color-muted)" }}
        />
      </div>
      <p className="mt-4 text-xs opacity-60">
        Auto-synthesized notes will appear here as you learn.
      </p>
    </div>
  );
}
