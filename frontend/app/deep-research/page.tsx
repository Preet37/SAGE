"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { getToken } from "@/lib/auth";
import { API_URL } from "@/lib/api";
import {
  Loader2,
  Search,
  Send,
  Mail,
  CheckCircle2,
  AlertTriangle,
  ExternalLink,
} from "lucide-react";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

interface StreamEvent {
  agent: "research" | "validator" | "concierge" | "orchestrator";
  kind: string;
  payload: Record<string, any>;
}

interface Expert {
  id: string;
  name: string;
  role?: string | null;
  organization?: string | null;
  h_index?: number | null;
  works_count?: number | null;
  cited_by_count?: number | null;
  relevance: number;
  email?: string | null;
  email_confidence?: number | null;
  apollo_data?: Record<string, any>;
}

interface Validation {
  confidence_score: number;
  citation_density: number;
  cross_source_agreement: number;
  recency_score: number;
  author_credibility: number;
  conflicting_evidence: string[];
  recommended_next_queries: string[];
  summary: string;
}

interface PaperNode {
  id: string;
  type: string;
  label: string;
  metadata: { year?: number; cited_by_count?: number; doi?: string; concepts?: string[] };
}

function authHeaders(): HeadersInit {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

function GoldBtn({
  onClick,
  disabled,
  children,
}: {
  onClick?: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...mono,
        fontSize: "0.55rem",
        letterSpacing: "0.14em",
        textTransform: "uppercase",
        padding: "0.55rem 1rem",
        background: disabled ? "rgba(196,152,90,0.3)" : "var(--gold)",
        color: disabled ? "var(--cream-2)" : "var(--ink)",
        border: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        display: "inline-flex",
        alignItems: "center",
        gap: "0.45rem",
      }}
    >
      {children}
    </button>
  );
}

function OutlineBtn({
  onClick,
  disabled,
  children,
}: {
  onClick?: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...mono,
        fontSize: "0.5rem",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        padding: "0.4rem 0.75rem",
        background: "none",
        color: disabled ? "var(--cream-2)" : "var(--cream-1)",
        border: "1px solid rgba(240,233,214,0.18)",
        cursor: disabled ? "not-allowed" : "pointer",
      }}
    >
      {children}
    </button>
  );
}

export default function DeepResearchPage() {
  const router = useRouter();
  const [topic, setTopic] = useState("");
  const [running, setRunning] = useState(false);
  const [runId, setRunId] = useState<string | null>(null);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  // Activity log is hidden in the UI but we still capture events to drive
  // the result cards (research/validation/expert handlers).
  const [phase, setPhase] = useState<string>("idle");
  const [papers, setPapers] = useState<PaperNode[]>([]);
  const [validation, setValidation] = useState<Validation | null>(null);
  const [experts, setExperts] = useState<Expert[]>([]);
  const [outreachExpert, setOutreachExpert] = useState<Expert | null>(null);
  const [emailSubject, setEmailSubject] = useState("");
  const [emailBody, setEmailBody] = useState("");
  const [sendingEmail, setSendingEmail] = useState(false);
  const [emailResult, setEmailResult] = useState<string | null>(null);
  const eventsScrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!getToken()) router.push("/login?returnTo=/deep-research");
  }, [router]);

  // Auto-scroll the activity log
  useEffect(() => {
    eventsScrollRef.current?.scrollTo({
      top: eventsScrollRef.current.scrollHeight,
    });
  }, [events]);

  const startRun = useCallback(async () => {
    if (!topic.trim() || running) return;
    setRunning(true);
    setEvents([]);
    setPapers([]);
    setValidation(null);
    setExperts([]);
    setPhase("starting");

    const res = await fetch(`${API_URL}/deep-research/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ topic, depth: 2, max_papers: 25 }),
    });
    if (!res.ok) {
      setRunning(false);
      setPhase("error");
      return;
    }
    const { run_id } = (await res.json()) as { run_id: string };
    setRunId(run_id);

    // Subscribe to SSE stream
    const t = getToken();
    const url = `${API_URL}/deep-research/runs/${run_id}/stream`;
    // EventSource doesn't support custom headers, so we use fetch+stream.
    try {
      const r = await fetch(url, { headers: authHeaders() });
      if (!r.body) {
        setRunning(false);
        return;
      }
      const reader = r.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split("\n\n");
        buffer = chunks.pop() || "";
        for (const chunk of chunks) {
          const dataLine = chunk
            .split("\n")
            .find((l) => l.startsWith("data: "));
          if (!dataLine) continue;
          try {
            const ev = JSON.parse(dataLine.slice(6)) as StreamEvent;
            handleEvent(ev);
          } catch {
            /* skip malformed */
          }
        }
      }
    } finally {
      setRunning(false);
    }
  }, [topic, running]);

  function handleEvent(ev: StreamEvent) {
    setEvents((prev) => [...prev, ev]);
    if (ev.agent === "orchestrator" && ev.kind === "phase") {
      setPhase(ev.payload.phase);
    }
    if (ev.agent === "research" && ev.kind === "done") {
      const g = ev.payload.graph as { nodes: PaperNode[] };
      const ps = (g?.nodes || []).filter((n) => n.type === "paper");
      // Sort by citations desc
      ps.sort(
        (a, b) =>
          (b.metadata.cited_by_count || 0) - (a.metadata.cited_by_count || 0)
      );
      setPapers(ps);
    }
    if (ev.agent === "validator" && ev.kind === "validation") {
      setValidation(ev.payload as Validation);
    }
    if (ev.agent === "concierge" && ev.kind === "expert") {
      setExperts((prev) => {
        // De-dupe by id; replace if same id (later events may add email)
        const idx = prev.findIndex((x) => x.id === ev.payload.id);
        if (idx >= 0) {
          const next = prev.slice();
          next[idx] = ev.payload as Expert;
          return next;
        }
        return [...prev, ev.payload as Expert];
      });
    }
  }

  const sendOutreach = useCallback(async () => {
    if (!outreachExpert || !runId) return;
    setSendingEmail(true);
    setEmailResult(null);
    const res = await fetch(
      `${API_URL}/deep-research/runs/${runId}/outreach`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({
          expert_id: outreachExpert.id,
          subject: emailSubject,
          body: emailBody,
        }),
      }
    );
    const result = await res.json().catch(() => ({}));
    setSendingEmail(false);
    if (res.ok && result.sent) {
      setEmailResult(`Sent (status ${result.status_code}).`);
    } else {
      setEmailResult(`Failed: ${result.error || result.detail || "unknown error"}`);
    }
  }, [outreachExpert, runId, emailSubject, emailBody]);

  function openOutreach(expert: Expert) {
    setOutreachExpert(expert);
    setEmailSubject(`Quick question on ${topic}`);
    setEmailBody(
      `Hello ${expert.name.split(" ")[0]},

I'm researching "${topic}" and your work has been highlighted by our system as among the most relevant in this area${expert.cited_by_count ? ` (${expert.cited_by_count.toLocaleString()} total citations)` : ""}.

I'd love to ask you a few short questions about your perspective on this topic — would you be open to a 15 minute call, or could I send a couple of questions over email?

Thank you for your time,
SAGE Deep Research`
    );
    setEmailResult(null);
  }

  return (
    <div
      className="flex flex-col h-screen"
      style={{ background: "var(--ink)", color: "var(--cream-0)" }}
    >
      <AppHeader />

      <div className="flex-1 overflow-y-auto thin-scrollbar">
        <div
          style={{
            maxWidth: "76rem",
            margin: "0 auto",
            padding: "2.5rem 1.5rem 4rem",
          }}
        >
          {/* Header */}
          <div style={{ marginBottom: "2rem" }}>
            <p
              style={{
                ...mono,
                fontSize: "0.58rem",
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                color: "var(--gold)",
                marginBottom: "0.5rem",
              }}
            >
              Deep Research
            </p>
            <h1
              style={{
                ...serif,
                fontSize: "2.4rem",
                fontWeight: 400,
                color: "var(--cream-0)",
                marginBottom: "0.5rem",
              }}
            >
              Multi-agent research & expert outreach
            </h1>
            <p
              style={{
                ...body,
                fontSize: "1rem",
                color: "var(--cream-2)",
                maxWidth: "40rem",
              }}
            >
              Three Fetch.ai-style agents work in concert: a Research Agent
              builds a citation knowledge graph from OpenAlex + Tavily, a
              Validator scores its credibility, and a Concierge surfaces and
              emails the most relevant experts via SendGrid.
            </p>
          </div>

          {/* Topic input */}
          <div
            style={{
              border: "1px solid rgba(240,233,214,0.12)",
              padding: "1.25rem",
              marginBottom: "1.5rem",
              background: "rgba(240,233,214,0.02)",
            }}
          >
            <label
              style={{
                ...mono,
                fontSize: "0.55rem",
                letterSpacing: "0.14em",
                textTransform: "uppercase",
                color: "var(--cream-2)",
                display: "block",
                marginBottom: "0.5rem",
              }}
            >
              Research topic
            </label>
            <div
              style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}
            >
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && startRun()}
                disabled={running}
                placeholder='e.g. "retrieval-augmented generation in education"'
                style={{
                  ...body,
                  flex: 1,
                  background: "transparent",
                  border: "1px solid rgba(240,233,214,0.18)",
                  padding: "0.6rem 0.85rem",
                  color: "var(--cream-0)",
                  fontSize: "1rem",
                  outline: "none",
                }}
              />
              <GoldBtn onClick={startRun} disabled={!topic.trim() || running}>
                {running ? (
                  <>
                    <Loader2
                      style={{ width: "0.8rem", height: "0.8rem" }}
                      className="animate-spin"
                    />
                    Running
                  </>
                ) : (
                  <>
                    <Search style={{ width: "0.8rem", height: "0.8rem" }} />
                    Start Run
                  </>
                )}
              </GoldBtn>
            </div>
            {phase !== "idle" && (
              <div
                style={{
                  ...mono,
                  fontSize: "0.55rem",
                  letterSpacing: "0.14em",
                  textTransform: "uppercase",
                  color: "var(--gold)",
                  marginTop: "0.75rem",
                }}
              >
                Phase: {phase}
              </div>
            )}
          </div>

          {/* Results */}
          {(events.length > 0 || running) && (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}
            >
              {validation && <ValidationCard v={validation} />}
              {papers.length > 0 && <PapersCard papers={papers} />}
              {experts.length > 0 && (
                <ExpertsCard experts={experts} onContact={openOutreach} />
              )}
              {running && experts.length === 0 && papers.length === 0 && (
                <div
                  style={{
                    ...mono,
                    fontSize: "0.6rem",
                    letterSpacing: "0.12em",
                    color: "var(--cream-2)",
                    padding: "2rem",
                    textAlign: "center",
                    border: "1px solid rgba(240,233,214,0.08)",
                  }}
                >
                  <Loader2
                    style={{
                      display: "inline-block",
                      width: "0.8rem",
                      height: "0.8rem",
                      marginRight: "0.5rem",
                    }}
                    className="animate-spin"
                  />
                  Searching OpenAlex, validating, and identifying experts…
                </div>
              )}
            </div>
          )}

          {/* Outreach modal */}
          {outreachExpert && (
            <div
              style={{
                position: "fixed",
                inset: 0,
                background: "rgba(0,0,0,0.7)",
                zIndex: 50,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "1rem",
              }}
              onClick={() => !sendingEmail && setOutreachExpert(null)}
            >
              <div
                onClick={(e) => e.stopPropagation()}
                style={{
                  background: "var(--ink-2)",
                  border: "1px solid rgba(240,233,214,0.12)",
                  maxWidth: "40rem",
                  width: "100%",
                  padding: "1.5rem",
                }}
              >
                <p
                  style={{
                    ...mono,
                    fontSize: "0.55rem",
                    letterSpacing: "0.14em",
                    textTransform: "uppercase",
                    color: "var(--gold)",
                    marginBottom: "0.4rem",
                  }}
                >
                  Outreach
                </p>
                <h2
                  style={{
                    ...serif,
                    fontSize: "1.6rem",
                    color: "var(--cream-0)",
                    marginBottom: "0.25rem",
                  }}
                >
                  {outreachExpert.name}
                </h2>
                <p
                  style={{
                    ...body,
                    fontSize: "0.85rem",
                    color: "var(--cream-2)",
                    marginBottom: "0.4rem",
                  }}
                >
                  {outreachExpert.role || "Researcher"}
                  {outreachExpert.organization
                    ? ` · ${outreachExpert.organization}`
                    : ""}
                </p>
                <p
                  style={{
                    ...mono,
                    fontSize: "0.6rem",
                    color: "var(--cream-2)",
                    marginBottom: "1rem",
                  }}
                >
                  → {outreachExpert.email}
                </p>

                <label
                  style={{
                    ...mono,
                    fontSize: "0.55rem",
                    letterSpacing: "0.14em",
                    textTransform: "uppercase",
                    color: "var(--cream-2)",
                    display: "block",
                    marginBottom: "0.35rem",
                  }}
                >
                  Subject
                </label>
                <input
                  value={emailSubject}
                  onChange={(e) => setEmailSubject(e.target.value)}
                  style={{
                    ...body,
                    width: "100%",
                    background: "transparent",
                    border: "1px solid rgba(240,233,214,0.18)",
                    padding: "0.5rem 0.7rem",
                    color: "var(--cream-0)",
                    marginBottom: "0.85rem",
                  }}
                />
                <label
                  style={{
                    ...mono,
                    fontSize: "0.55rem",
                    letterSpacing: "0.14em",
                    textTransform: "uppercase",
                    color: "var(--cream-2)",
                    display: "block",
                    marginBottom: "0.35rem",
                  }}
                >
                  Body
                </label>
                <textarea
                  value={emailBody}
                  onChange={(e) => setEmailBody(e.target.value)}
                  rows={10}
                  style={{
                    ...body,
                    width: "100%",
                    background: "transparent",
                    border: "1px solid rgba(240,233,214,0.18)",
                    padding: "0.5rem 0.7rem",
                    color: "var(--cream-0)",
                    resize: "vertical",
                    marginBottom: "1rem",
                  }}
                />

                <div
                  style={{
                    display: "flex",
                    gap: "0.5rem",
                    justifyContent: "flex-end",
                    alignItems: "center",
                  }}
                >
                  {emailResult && (
                    <span
                      style={{
                        ...mono,
                        fontSize: "0.55rem",
                        color: emailResult.startsWith("Sent")
                          ? "var(--gold)"
                          : "#ff6b6b",
                        marginRight: "auto",
                      }}
                    >
                      {emailResult}
                    </span>
                  )}
                  <OutlineBtn
                    onClick={() => setOutreachExpert(null)}
                    disabled={sendingEmail}
                  >
                    Cancel
                  </OutlineBtn>
                  <GoldBtn onClick={sendOutreach} disabled={sendingEmail}>
                    {sendingEmail ? (
                      <>
                        <Loader2
                          style={{ width: "0.8rem", height: "0.8rem" }}
                          className="animate-spin"
                        />
                        Sending
                      </>
                    ) : (
                      <>
                        <Send style={{ width: "0.8rem", height: "0.8rem" }} />
                        Send via SendGrid
                      </>
                    )}
                  </GoldBtn>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function EventLine({ event }: { event: StreamEvent }) {
  const colorByAgent: Record<string, string> = {
    research: "#a3c4ff",
    validator: "#c499ff",
    concierge: "#ffd28a",
    orchestrator: "var(--gold)",
  };
  const accent = colorByAgent[event.agent] || "var(--cream-2)";
  const msg =
    event.payload.message ||
    (event.kind === "graph_update"
      ? `Graph: ${event.payload.nodes} nodes, ${event.payload.edges} edges`
      : event.kind === "validation"
      ? `Validation confidence: ${(event.payload.confidence_score ?? 0).toFixed(2)}`
      : event.kind === "expert"
      ? `Expert: ${event.payload.name}${event.payload.email ? ` (${event.payload.email})` : ""}`
      : event.kind === "phase"
      ? `→ ${event.payload.phase}`
      : event.kind === "tavily"
      ? `Tavily: ${event.payload.results?.length ?? 0} sources`
      : event.kind);
  return (
    <div
      style={{
        ...mono,
        fontSize: "0.6rem",
        padding: "0.35rem 1rem",
        borderLeft: `2px solid ${accent}`,
        marginLeft: "0.6rem",
        color: "var(--cream-1)",
      }}
    >
      <span style={{ color: accent, marginRight: "0.5rem" }}>
        [{event.agent}]
      </span>
      {msg}
    </div>
  );
}

function ValidationCard({ v }: { v: Validation }) {
  const conf = (v.confidence_score * 100).toFixed(0);
  const Bar = ({ label, value }: { label: string; value: number }) => (
    <div style={{ marginBottom: "0.5rem" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          ...mono,
          fontSize: "0.55rem",
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          color: "var(--cream-2)",
          marginBottom: "0.2rem",
        }}
      >
        <span>{label}</span>
        <span>{(value * 100).toFixed(0)}%</span>
      </div>
      <div
        style={{
          height: "3px",
          background: "rgba(240,233,214,0.08)",
        }}
      >
        <div
          style={{
            width: `${value * 100}%`,
            height: "100%",
            background: "var(--gold)",
          }}
        />
      </div>
    </div>
  );
  return (
    <div
      style={{
        border: "1px solid rgba(240,233,214,0.12)",
        background: "rgba(240,233,214,0.02)",
        padding: "1rem 1.1rem",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          justifyContent: "space-between",
          marginBottom: "0.6rem",
        }}
      >
        <span
          style={{
            ...mono,
            fontSize: "0.55rem",
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--cream-2)",
          }}
        >
          Validation report
        </span>
        <span
          style={{ ...serif, fontSize: "1.7rem", color: "var(--gold)" }}
        >
          {conf}%
        </span>
      </div>
      <p
        style={{
          ...body,
          fontSize: "0.85rem",
          color: "var(--cream-1)",
          marginBottom: "0.85rem",
        }}
      >
        {v.summary}
      </p>
      <Bar label="Citation density" value={v.citation_density} />
      <Bar label="Recency" value={v.recency_score} />
      <Bar label="Author credibility" value={v.author_credibility} />
      <Bar label="Cross-source agreement" value={v.cross_source_agreement} />
      {v.conflicting_evidence.length > 0 && (
        <div style={{ marginTop: "0.75rem" }}>
          <p
            style={{
              ...mono,
              fontSize: "0.55rem",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: "#ff9b6b",
              marginBottom: "0.3rem",
            }}
          >
            <AlertTriangle
              style={{
                display: "inline",
                width: "0.7rem",
                height: "0.7rem",
                marginRight: "0.3rem",
              }}
            />
            Conflicts
          </p>
          {v.conflicting_evidence.map((c, i) => (
            <p
              key={i}
              style={{
                ...body,
                fontSize: "0.8rem",
                color: "var(--cream-2)",
              }}
            >
              · {c}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

function PapersCard({ papers }: { papers: PaperNode[] }) {
  return (
    <div
      style={{
        border: "1px solid rgba(240,233,214,0.12)",
        background: "rgba(240,233,214,0.02)",
      }}
    >
      <div
        style={{
          ...mono,
          fontSize: "0.55rem",
          letterSpacing: "0.14em",
          textTransform: "uppercase",
          color: "var(--cream-2)",
          padding: "0.85rem 1rem",
          borderBottom: "1px solid rgba(240,233,214,0.08)",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>Top papers</span>
        <span>{papers.length}</span>
      </div>
      <div style={{ maxHeight: "20rem", overflowY: "auto" }} className="thin-scrollbar">
        {papers.slice(0, 15).map((p) => (
          <a
            key={p.id}
            href={p.id}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "block",
              padding: "0.7rem 1rem",
              borderBottom: "1px solid rgba(240,233,214,0.05)",
              textDecoration: "none",
              color: "var(--cream-0)",
            }}
          >
            <div
              style={{
                ...body,
                fontSize: "0.92rem",
                color: "var(--cream-0)",
                marginBottom: "0.2rem",
              }}
            >
              {p.label}
            </div>
            <div
              style={{
                ...mono,
                fontSize: "0.55rem",
                color: "var(--cream-2)",
              }}
            >
              {p.metadata.year || "—"} ·{" "}
              {(p.metadata.cited_by_count || 0).toLocaleString()} citations
              {p.metadata.concepts && p.metadata.concepts.length
                ? ` · ${p.metadata.concepts.slice(0, 3).join(", ")}`
                : ""}
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

function ExpertsCard({
  experts,
  onContact,
}: {
  experts: Expert[];
  onContact: (e: Expert) => void;
}) {
  return (
    <div
      style={{
        border: "1px solid rgba(240,233,214,0.12)",
        background: "rgba(240,233,214,0.02)",
      }}
    >
      <div
        style={{
          ...mono,
          fontSize: "0.55rem",
          letterSpacing: "0.14em",
          textTransform: "uppercase",
          color: "var(--cream-2)",
          padding: "0.85rem 1rem",
          borderBottom: "1px solid rgba(240,233,214,0.08)",
        }}
      >
        Experts ({experts.length})
      </div>
      {experts.map((e) => (
        <div
          key={e.id}
          style={{
            padding: "0.85rem 1rem",
            borderBottom: "1px solid rgba(240,233,214,0.05)",
            display: "flex",
            gap: "0.75rem",
            alignItems: "center",
          }}
        >
          <div style={{ flex: 1 }}>
            <div
              style={{
                ...serif,
                fontSize: "1.15rem",
                color: "var(--cream-0)",
              }}
            >
              {e.name}
            </div>
            <div
              style={{
                ...body,
                fontSize: "0.82rem",
                color: "var(--cream-2)",
                marginTop: "0.1rem",
              }}
            >
              {e.role || (e.organization ? "Researcher" : "")}
              {e.organization ? ` · ${e.organization}` : ""}
            </div>
            <div
              style={{
                ...mono,
                fontSize: "0.55rem",
                color: "var(--cream-2)",
                marginTop: "0.25rem",
              }}
            >
              h-index: {e.h_index ?? "—"} ·{" "}
              {(e.cited_by_count ?? 0).toLocaleString()} citations · relevance{" "}
              {e.relevance.toFixed(0)}
            </div>
            {e.email && (
              <div
                style={{
                  ...mono,
                  fontSize: "0.55rem",
                  color: "var(--gold)",
                  marginTop: "0.25rem",
                }}
              >
                <CheckCircle2
                  style={{
                    display: "inline",
                    width: "0.7rem",
                    height: "0.7rem",
                    marginRight: "0.3rem",
                  }}
                />
                {e.email}
                {e.email_confidence != null
                  ? ` (${(e.email_confidence * 100).toFixed(0)}% confidence)`
                  : ""}
              </div>
            )}
          </div>
          <GoldBtn onClick={() => onContact(e)} disabled={!e.email}>
            <Mail style={{ width: "0.8rem", height: "0.8rem" }} />
            Contact
          </GoldBtn>
        </div>
      ))}
    </div>
  );
}
