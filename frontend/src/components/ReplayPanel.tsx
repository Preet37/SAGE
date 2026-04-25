"use client";

import { useEffect, useState } from "react";

import {
  getReplay,
  type AgentTrace,
  type ReplaySession,
  type TutorMessageRow,
} from "@/lib/api";

interface ReplayPanelProps {
  sessionId: number;
  token: string;
  refreshKey?: number;
}

export default function ReplayPanel({ sessionId, token, refreshKey = 0 }: ReplayPanelProps) {
  const [data, setData] = useState<ReplaySession | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [openTrace, setOpenTrace] = useState<number | null>(null);

  useEffect(() => {
    if (!token) return;
    getReplay(sessionId, token)
      .then(setData)
      .catch((err) => setError(String(err)));
  }, [sessionId, token, refreshKey]);

  return (
    <div className="card flex h-full flex-col p-5">
      <header>
        <h3 className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          Replay
        </h3>
        <p className="mt-1 text-xs opacity-70">
          {data
            ? `Started ${new Date(data.started_at).toLocaleString()} · ${data.messages.length} message(s)`
            : "Loading…"}
        </p>
      </header>

      {error && (
        <p role="alert" className="mt-2 text-xs" style={{ color: "var(--color-destructive)" }}>
          {error}
        </p>
      )}

      <ol className="mt-3 flex-1 space-y-2 overflow-auto pr-1 text-sm">
        {data && data.messages.length === 0 && (
          <li
            className="rounded-2xl px-3 py-2 text-xs opacity-70"
            style={{ background: "var(--color-muted)" }}
          >
            No turns yet — ask SAGE something to populate this view.
          </li>
        )}
        {data?.messages.map((m) => (
          <li
            key={m.id}
            className="rounded-2xl border p-3"
            style={{ borderColor: "var(--color-border)" }}
          >
            <div className="flex items-center justify-between">
              <p className="text-xs font-semibold opacity-70">
                {m.role === "user" ? "You" : "SAGE"}
                <span className="ml-2 opacity-60">
                  {new Date(m.created_at).toLocaleTimeString()}
                </span>
              </p>
              {m.role === "assistant" && (
                <Verdict
                  passed={m.verification_passed}
                  score={m.verification_score}
                  flagCount={m.verification_flags.length}
                />
              )}
            </div>
            <p className="mt-1 whitespace-pre-wrap">{m.content}</p>

            {m.role === "assistant" && hasTrace(m.agent_trace) && (
              <>
                <button
                  type="button"
                  onClick={() => setOpenTrace((v) => (v === m.id ? null : m.id))}
                  className="mt-2 text-xs font-semibold"
                  style={{ color: "var(--color-primary)" }}
                >
                  {openTrace === m.id ? "Hide agent trace" : "Show agent trace"}
                </button>
                {openTrace === m.id && <TraceView trace={m.agent_trace} />}
              </>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}

function hasTrace(t: AgentTrace): boolean {
  return Boolean(
    t.plan ||
      t.concept_map_delta?.length ||
      t.assessment ||
      (t.peers && t.peers.length) ||
      t.progress_delta,
  );
}

function Verdict({
  passed,
  score,
  flagCount,
}: {
  passed: boolean;
  score: number;
  flagCount: number;
}) {
  return (
    <span
      className="rounded-full px-2 py-0.5 text-xs font-semibold"
      style={{
        background: passed ? "var(--color-muted)" : "color-mix(in srgb, var(--color-destructive) 15%, white)",
        color: passed ? "var(--color-primary)" : "var(--color-destructive)",
      }}
    >
      {passed ? "✓" : "⚠"} {score.toFixed(2)}
      {flagCount > 0 && <span style={{ opacity: 0.7 }}> · {flagCount} flag(s)</span>}
    </span>
  );
}

function TraceView({ trace }: { trace: AgentTrace }) {
  return (
    <dl className="mt-2 grid grid-cols-1 gap-1 text-xs">
      {trace.teaching_mode && (
        <Row label="Mode" value={trace.teaching_mode} />
      )}
      {trace.plan && (
        <Row
          label="Plan"
          value={`${stringField(trace.plan, "strategy")} · ${stringField(trace.plan, "depth")}`}
        />
      )}
      {trace.concept_map_delta && trace.concept_map_delta.length > 0 && (
        <Row
          label="New concepts"
          value={trace.concept_map_delta.map((c) => c.label).join(", ")}
        />
      )}
      {trace.assessment?.question && (
        <Row label="Check" value={trace.assessment.question} />
      )}
      {trace.peers && trace.peers.length > 0 && (
        <Row label="Peers" value={`${trace.peers.length} suggested`} />
      )}
      {trace.progress_delta && typeof trace.progress_delta.bump === "number" && (
        <Row label="Mastery bump" value={trace.progress_delta.bump.toFixed(3)} />
      )}
    </dl>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-3">
      <dt className="opacity-70">{label}</dt>
      <dd className="text-right font-semibold">{value}</dd>
    </div>
  );
}

function stringField(obj: Record<string, unknown>, key: string): string {
  const v = obj[key];
  return typeof v === "string" ? v : "—";
}

// Optional re-export so other components can render a single message identically.
export type { TutorMessageRow };
