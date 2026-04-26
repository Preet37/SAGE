"use client";
import { useState, useEffect, useRef } from "react";
import { getToken } from "@/lib/auth";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { PenLine, Sparkles, BarChart2, Download, Save, Loader2 } from "lucide-react";

interface Props {
  lessonId: string;
  lessonTitle?: string;
  concepts?: string[];
}

interface RevisionResult {
  original: string;
  revised: string;
  gaps_identified: string[];
  concept_connections: { from: string; to: string; relationship: string }[];
  misconceptions: string[];
  strength_score: number;
  suggestions: string[];
}

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

export function NotesPanel({ lessonId, lessonTitle, concepts }: Props) {
  const STORAGE_KEY = `sage-notes-${lessonId}`;
  const [notes, setNotes] = useState("");
  const [result, setResult] = useState<RevisionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"write" | "revised" | "analysis">("write");
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const saveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const data = JSON.parse(raw);
        if (data.notes) setNotes(data.notes);
        if (data.result) setResult(data.result);
        if (data.saved_at) setSavedAt(data.saved_at);
      }
    } catch { /* ignore */ }
  }, [lessonId, STORAGE_KEY]);

  useEffect(() => {
    if (!notes.trim()) return;
    if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
    saveTimerRef.current = setTimeout(() => {
      const ts = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ notes, result, saved_at: ts }));
      setSavedAt(ts);
    }, 1000);
    return () => { if (saveTimerRef.current) clearTimeout(saveTimerRef.current); };
  }, [notes, result, STORAGE_KEY]);

  async function handleRevise() {
    if (!notes.trim()) return;
    const token = getToken();
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/notes/revise`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ lesson_id: lessonId, content: notes, lesson_title: lessonTitle, concepts }),
      });
      const data = await res.json();
      setResult(data);
      setActiveTab("revised");
      const ts = new Date().toISOString();
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ notes, result: data, saved_at: ts }));
      setSavedAt(ts);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  function downloadNotes() {
    const content = result
      ? `# My Notes — ${lessonTitle || "Lesson"}\n\n## My Original Notes\n${notes}\n\n## AI Revised Version\n${result.revised}\n\n## Knowledge Gaps\n${result.gaps_identified.map(g => `- ${g}`).join("\n")}\n\n## Suggestions\n${result.suggestions.map(s => `- ${s}`).join("\n")}`
      : `# My Notes — ${lessonTitle || "Lesson"}\n\n${notes}`;
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `notes-${lessonId}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  const tabs = [
    { id: "write" as const, label: "Write", icon: PenLine },
    { id: "revised" as const, label: "AI Revised", icon: Sparkles },
    { id: "analysis" as const, label: "Analysis", icon: BarChart2 },
  ];

  const score = result?.strength_score ?? 0;
  const scoreColor = score >= 0.7 ? "var(--sage-c)" : score >= 0.4 ? "var(--gold)" : "var(--rose)";

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", padding: "1.25rem 1.25rem 1.5rem" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1rem", flexShrink: 0 }}>
        <div>
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>
            Notes & AI Revision
          </p>
          {savedAt && (
            <p style={{ ...mono, fontSize: "0.42rem", color: "var(--cream-2)", opacity: 0.6, marginTop: "0.15rem" }}>
              ✓ saved {new Date(savedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </p>
          )}
        </div>
        <button
          onClick={downloadNotes}
          style={{ ...mono, display: "flex", alignItems: "center", gap: "0.3rem", fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--cream-2)", background: "none", border: "1px solid rgba(240,233,214,0.1)", padding: "0.3rem 0.6rem", cursor: "pointer" }}
        >
          <Download style={{ width: "0.65rem", height: "0.65rem" }} />
          Export
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid rgba(240,233,214,0.07)", marginBottom: "1rem", flexShrink: 0 }}>
        {tabs.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            style={{ ...mono, display: "flex", alignItems: "center", gap: "0.3rem", fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", padding: "0.5rem 0.75rem", background: "none", border: "none", borderBottom: activeTab === id ? "2px solid var(--gold)" : "2px solid transparent", color: activeTab === id ? "var(--cream-0)" : "var(--cream-2)", cursor: "pointer", transition: "all 0.15s" }}
          >
            <Icon style={{ width: "0.6rem", height: "0.6rem" }} />
            {label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" }}>
        {activeTab === "write" && (
          <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={`Write your notes here — explain concepts in your own words.\n\nFor example:\n- Attention works by...\n- The key difference from RNNs is...\n- I'm confused about...`}
              style={{ flex: 1, background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "1rem", ...body, fontSize: "0.9rem", color: "var(--cream-0)", lineHeight: 1.7, resize: "none", outline: "none", minHeight: "200px" }}
            />
            <button
              onClick={handleRevise}
              disabled={loading || !notes.trim()}
              style={{ ...mono, display: "flex", alignItems: "center", justifyContent: "center", gap: "0.5rem", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.75rem", background: "rgba(196,152,90,0.12)", border: "1px solid rgba(196,152,90,0.3)", color: "var(--gold)", cursor: loading || !notes.trim() ? "not-allowed" : "pointer", opacity: loading || !notes.trim() ? 0.5 : 1, transition: "all 0.15s" }}
            >
              {loading ? (
                <><Loader2 style={{ width: "0.65rem", height: "0.65rem" }} className="animate-spin" /> AI is reviewing…</>
              ) : (
                <><Sparkles style={{ width: "0.65rem", height: "0.65rem" }} /> Get AI Revision</>
              )}
            </button>
          </div>
        )}

        {activeTab === "revised" && (
          <div style={{ flex: 1, overflowY: "auto" }}>
            {result ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                {/* Score */}
                <div style={{ display: "flex", alignItems: "center", gap: "1rem", padding: "0.85rem 1rem", background: "var(--ink-1)", border: `1px solid ${scoreColor}30` }}>
                  <span style={{ fontFamily: "var(--font-cormorant)", fontWeight: 700, fontSize: "2rem", color: scoreColor, lineHeight: 1 }}>
                    {Math.round(score * 100)}%
                  </span>
                  <div>
                    <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: scoreColor }}>Note Strength</p>
                    <p style={{ ...body, fontSize: "0.8rem", color: "var(--cream-2)" }}>
                      {score >= 0.7 ? "Strong understanding" : score >= 0.4 ? "Developing — keep going" : "Needs more depth"}
                    </p>
                  </div>
                </div>

                {/* Revised notes */}
                <div style={{ padding: "0.85rem 1rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", borderLeft: "3px solid var(--sage-c)" }}>
                  <p style={{ ...mono, fontSize: "0.43rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--sage-c)", marginBottom: "0.6rem" }}>AI Revised Version</p>
                  <div className="prose prose-invert prose-sm max-w-none prose-p:my-1.5 prose-p:leading-[1.7]" style={{ color: "var(--cream-0)", ...body }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.revised}</ReactMarkdown>
                  </div>
                </div>
              </div>
            ) : (
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", ...body, fontSize: "0.9rem", color: "var(--cream-2)" }}>
                Write notes and click "Get AI Revision" first
              </div>
            )}
          </div>
        )}

        {activeTab === "analysis" && (
          <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            {result ? (
              <>
                {result.misconceptions.length > 0 && (
                  <Section color="var(--rose)" label="Misconceptions Detected">
                    {result.misconceptions.map((m, i) => (
                      <p key={i} style={{ ...body, fontSize: "0.85rem", color: "var(--cream-1)", display: "flex", gap: "0.5rem" }}>
                        <span style={{ color: "var(--rose)" }}>✗</span> {m}
                      </p>
                    ))}
                  </Section>
                )}
                {result.gaps_identified.length > 0 && (
                  <Section color="var(--gold)" label="Knowledge Gaps">
                    {result.gaps_identified.map((g, i) => (
                      <p key={i} style={{ ...body, fontSize: "0.85rem", color: "var(--cream-1)", display: "flex", gap: "0.5rem" }}>
                        <span style={{ color: "var(--gold)" }}>○</span> {g}
                      </p>
                    ))}
                  </Section>
                )}
                {result.concept_connections.length > 0 && (
                  <Section color="var(--sage-c)" label="Concept Connections">
                    {result.concept_connections.map((c, i) => (
                      <div key={i} style={{ marginBottom: "0.5rem" }}>
                        <p style={{ ...mono, fontSize: "0.48rem", color: "var(--cream-0)" }}>
                          <span style={{ color: "var(--sage-c)" }}>{c.from}</span>
                          <span style={{ color: "var(--cream-2)", margin: "0 0.4rem" }}>→</span>
                          <span style={{ color: "var(--gold)" }}>{c.to}</span>
                        </p>
                        <p style={{ ...body, fontSize: "0.78rem", color: "var(--cream-2)", marginLeft: "0.5rem" }}>{c.relationship}</p>
                      </div>
                    ))}
                  </Section>
                )}
                {result.suggestions.length > 0 && (
                  <Section color="var(--cream-1)" label="Suggestions">
                    {result.suggestions.map((s, i) => (
                      <p key={i} style={{ ...body, fontSize: "0.85rem", color: "var(--cream-1)", display: "flex", gap: "0.5rem" }}>
                        <span style={{ color: "var(--gold)" }}>→</span> {s}
                      </p>
                    ))}
                  </Section>
                )}
              </>
            ) : (
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", ...body, fontSize: "0.9rem", color: "var(--cream-2)" }}>
                Get AI revision first to see analysis
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function Section({ color, label, children }: { color: string; label: string; children: React.ReactNode }) {
  const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
  return (
    <div style={{ padding: "0.85rem 1rem", background: "var(--ink-1)", border: `1px solid ${color}25`, borderLeft: `3px solid ${color}` }}>
      <p style={{ ...mono, fontSize: "0.43rem", letterSpacing: "0.1em", textTransform: "uppercase", color, marginBottom: "0.6rem" }}>{label}</p>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.3rem" }}>{children}</div>
    </div>
  );
}
