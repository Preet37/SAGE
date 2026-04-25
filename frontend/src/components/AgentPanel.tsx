"use client";

import type { AgentEvent, AgentName } from "@/lib/api";

const AGENT_LABEL: Record<string, string> = {
  orchestrator: "Orchestrator",
  retriever: "Retriever",
  pedagogy: "Pedagogy",
  content: "Content",
  socratic: "Socratic",
  concept_map: "Concept Map",
  assessment: "Assessment",
  peer_match: "Peer Match",
  progress: "Progress",
  verifier: "Verifier",
};

const AGENT_DESC: Record<string, string> = {
  orchestrator: "Routing the swarm",
  retriever: "Pulling source chunks",
  pedagogy: "Choosing strategy",
  content: "Composing the answer",
  concept_map: "Extracting concepts",
  assessment: "Building a check",
  peer_match: "Suggesting study peers",
  progress: "Updating mastery",
};

const SLOTS: AgentName[] = [
  "pedagogy",
  "retriever",
  "content",
  "concept_map",
  "assessment",
  "progress",
];

export interface AgentSlotState {
  status: "idle" | "active" | "done" | "error";
  detail?: string;
}

export type AgentPanelState = Partial<Record<AgentName, AgentSlotState>>;

export function applyAgentEvent(
  state: AgentPanelState,
  e: AgentEvent,
): AgentPanelState {
  const detail = describe(e);
  const status: AgentSlotState["status"] = e.phase === "done" ? "done" : "active";
  return { ...state, [e.agent]: { status, detail } };
}

function describe(e: AgentEvent): string {
  switch (e.agent) {
    case "retriever":
      return e.phase === "retrieved" && typeof e.k === "number"
        ? `${e.k} chunks${e.scores?.length ? ` · top ${e.scores[0]}` : ""}`
        : "ready";
    case "pedagogy": {
      const plan = (e.plan ?? {}) as { strategy?: string; depth?: string };
      return plan.strategy ? `${plan.strategy} · ${plan.depth ?? ""}` : e.phase;
    }
    case "content":
      return typeof e.chars === "number" ? `${e.chars} chars` : e.phase;
    case "concept_map": {
      const arr = Array.isArray(e.delta) ? (e.delta as { label: string }[]) : [];
      return arr.length ? `+${arr.length} concept(s)` : e.phase;
    }
    case "assessment": {
      const data = (e.data ?? {}) as { skip?: boolean; concept?: string };
      return data.skip ? "skipped" : data.concept ? `target: ${data.concept}` : "ready";
    }
    case "peer_match": {
      const peers = Array.isArray(e.peers) ? (e.peers as unknown[]).length : 0;
      return peers ? `${peers} match(es)` : "no peers";
    }
    case "progress": {
      const delta = (e.delta ?? {}) as { bump?: number };
      return typeof delta.bump === "number" ? `bump ${delta.bump.toFixed(2)}` : e.phase;
    }
    default:
      return e.phase;
  }
}

export default function AgentPanel({ state }: { state: AgentPanelState }) {
  return (
    <div className="card flex h-full flex-col p-5">
      <header>
        <h3 className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          Agents
        </h3>
        <p className="mt-1 text-xs opacity-70">Live view of the six-agent swarm.</p>
      </header>
      <ul className="mt-3 flex-1 space-y-2 overflow-auto pr-1">
        {SLOTS.map((id) => {
          const s = state[id];
          const status = s?.status ?? "idle";
          return (
            <li
              key={id}
              className="flex items-center justify-between rounded-2xl border px-3 py-2"
              style={{
                borderColor: "var(--color-border)",
                background:
                  status === "active" ? "var(--color-muted)" : "white",
              }}
            >
              <div>
                <p className="text-sm font-semibold">{AGENT_LABEL[id]}</p>
                <p className="text-xs opacity-70">
                  {s?.detail ?? AGENT_DESC[id] ?? "—"}
                </p>
              </div>
              <Dot status={status} />
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function Dot({ status }: { status: AgentSlotState["status"] }) {
  if (status === "active") return <span className="pulse-dot" aria-hidden />;
  const color =
    status === "done"
      ? "var(--color-secondary)"
      : status === "error"
        ? "var(--color-destructive)"
        : "var(--color-border)";
  return <span aria-hidden className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: color }} />;
}
