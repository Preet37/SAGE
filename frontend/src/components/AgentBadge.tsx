"use client";

const AGENT_LABEL: Record<string, string> = {
  orchestrator: "Routing",
  retriever: "Retrieving sources",
  pedagogy: "Choosing strategy",
  content: "Composing answer",
  socratic: "Asking",
  concept_map: "Mapping concepts",
  assessment: "Building check",
  peer_match: "Matching peers",
  progress: "Updating mastery",
  verifier: "Verifying",
};

export default function AgentBadge({ active }: { active: string | null }) {
  if (!active) return null;
  const [agent, phase] = active.split(":");
  const label = AGENT_LABEL[agent] ?? agent;

  return (
    <div
      className="flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold"
      style={{
        background: "var(--color-muted)",
        color: "var(--color-primary)",
        border: "1px solid var(--color-border)",
      }}
    >
      <span className="pulse-dot" aria-hidden />
      <span>{label}</span>
      {phase && phase !== "done" && (
        <span style={{ opacity: 0.6 }}>· {phase}</span>
      )}
    </div>
  );
}
