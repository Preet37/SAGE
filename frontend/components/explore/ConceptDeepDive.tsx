"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, ConceptPageResponse, ConceptSuggestion, KeyEquation, ConceptPaper, ConceptVideo } from "@/lib/api";
import {
  Search,
  Loader2,
  Lightbulb,
  CheckCircle2,
  XCircle,
  ArrowLeft,
  ArrowRight,
  BookMarked,
  AlertTriangle,
  Star,
  Link2,
  Sparkles,
  FlaskConical,
  Youtube,
  GraduationCap,
  Network,
  ChevronRight,
  ExternalLink,
  Sigma,
} from "lucide-react";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

const card: React.CSSProperties = {
  background: "var(--ink-1)",
  border: "1px solid rgba(240,233,214,0.08)",
  padding: "1.25rem 1.5rem",
  marginBottom: "0.75rem",
};

const sectionLabel: React.CSSProperties = {
  ...mono,
  fontSize: "0.55rem",
  letterSpacing: "0.16em",
  textTransform: "uppercase",
  color: "var(--gold)",
  marginBottom: "0.75rem",
};

const sectionTitle: React.CSSProperties = {
  ...mono,
  fontSize: "0.6rem",
  letterSpacing: "0.14em",
  textTransform: "uppercase",
  color: "var(--cream-2)",
  marginBottom: "0.75rem",
  display: "flex",
  alignItems: "center",
  gap: "0.4rem",
};

function LevelBadge({ level }: { level: string }) {
  const cfg: Record<string, { color: string; border: string }> = {
    beginner:     { color: "var(--sage-c)",  border: "rgba(107,153,118,0.35)" },
    intermediate: { color: "var(--gold)",    border: "rgba(196,152,90,0.35)"  },
    advanced:     { color: "#f97316",        border: "rgba(249,115,22,0.35)"  },
  };
  const c = cfg[level] || cfg.intermediate;
  return (
    <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: c.color, border: `1px solid ${c.border}`, padding: "0.1rem 0.45rem" }}>
      {level}
    </span>
  );
}

function RevealSection({ index, children }: { index: number; children: React.ReactNode }) {
  return (
    <div className="animate-[fadeSlideIn_0.4s_ease-out_both]" style={{ animationDelay: `${index * 120}ms` }}>
      {children}
    </div>
  );
}

function ConceptWeb({ center, nodes, onNodeClick }: { center: string; nodes: string[]; onNodeClick: (n: string) => void }) {
  const r = 120;
  const cx = 180;
  const cy = 160;
  const displayed = nodes.slice(0, 8);

  return (
    <svg viewBox="0 0 360 320" style={{ width: "100%", maxHeight: "18rem", userSelect: "none" }}>
      {displayed.map((_, i) => {
        const angle = (2 * Math.PI * i) / displayed.length - Math.PI / 2;
        return (
          <line key={i} x1={cx} y1={cy} x2={cx + r * Math.cos(angle)} y2={cy + r * Math.sin(angle)}
            stroke="rgba(240,233,214,0.12)" strokeWidth={1.5} />
        );
      })}
      {displayed.map((label, i) => {
        const angle = (2 * Math.PI * i) / displayed.length - Math.PI / 2;
        const nx = cx + r * Math.cos(angle);
        const ny = cy + r * Math.sin(angle);
        const words = label.split(" ");
        return (
          <g key={i} style={{ cursor: "pointer" }} onClick={() => onNodeClick(label)}>
            <circle cx={nx} cy={ny} r={28} fill="var(--ink-2)" stroke="rgba(240,233,214,0.1)" strokeWidth={1.5} />
            <circle cx={nx} cy={ny} r={28} fill="rgba(196,152,90,0.04)" />
            {words.slice(0, 2).map((word, wi) => (
              <text key={wi} x={nx} y={ny + (words.length > 1 ? (wi - 0.5) * 11 : 4)}
                textAnchor="middle" fontSize={8} fill="rgba(240,233,214,0.7)">
                {word.length > 10 ? word.slice(0, 9) + "…" : word}
              </text>
            ))}
          </g>
        );
      })}
      <circle cx={cx} cy={cy} r={36} fill="rgba(196,152,90,0.12)" stroke="rgba(196,152,90,0.45)" strokeWidth={2} />
      {center.split(" ").slice(0, 3).map((word, i, arr) => (
        <text key={i} x={cx} y={cy + (i - (arr.length - 1) / 2) * 12 + 4}
          textAnchor="middle" fontSize={9} fontWeight="600" fill="var(--gold)">
          {word.length > 12 ? word.slice(0, 11) + "…" : word}
        </text>
      ))}
    </svg>
  );
}

export function ConceptDeepDive({ initialQuery = "" }: { initialQuery?: string }) {
  const router = useRouter();
  const [query, setQuery] = useState(initialQuery);
  const [concept, setConcept] = useState<ConceptPageResponse | null>(null);
  const [suggestions, setSuggestions] = useState<ConceptSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestionsLoading, setSuggestionsLoading] = useState(true);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [highlightIdx, setHighlightIdx] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    api.concepts.getSuggestions(token).then(setSuggestions).catch(() => {}).finally(() => setSuggestionsLoading(false));
  }, [router]);

  useEffect(() => {
    if (initialQuery) handleSearch(initialQuery);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredSuggestions = query.trim().length > 0
    ? suggestions.filter((s) => s.label.toLowerCase().includes(query.toLowerCase().trim()))
    : [];

  async function handleSearch(topic?: string) {
    const searchTopic = topic ?? query.trim();
    if (!searchTopic || loading) return;
    const token = getToken();
    if (!token) return;
    setQuery(searchTopic);
    setDropdownOpen(false);
    setHighlightIdx(-1);
    setLoading(true);
    setConcept(null);
    setError(null);
    try {
      const result = await api.concepts.search(searchTopic, token);
      setConcept(result);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Search failed";
      setError(
        msg.includes("Not Found")
          ? "Deep Dive search is not available on this backend."
          : msg.includes("LLM not configured") || msg.includes("LLM_API_KEY")
          ? "AI search requires an LLM API key. Set LLM_API_KEY in backend/.env and restart the server."
          : msg
      );
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (dropdownOpen && filteredSuggestions.length > 0) {
      if (e.key === "ArrowDown") { e.preventDefault(); setHighlightIdx((p) => Math.min(p + 1, filteredSuggestions.length - 1)); return; }
      if (e.key === "ArrowUp") { e.preventDefault(); setHighlightIdx((p) => Math.max(p - 1, -1)); return; }
      if (e.key === "Enter" && highlightIdx >= 0) { e.preventDefault(); handleSearch(filteredSuggestions[highlightIdx].label); return; }
      if (e.key === "Escape") { setDropdownOpen(false); return; }
    }
    if (e.key === "Enter") handleSearch();
  }

  function handleRelatedClick(topic: string) { setQuery(topic); handleSearch(topic); }

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) setDropdownOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div style={{ flex: 1, overflowY: "auto", minHeight: 0 }}>
      <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "2rem 1.5rem" }}>

        {/* Empty state header */}
        {!concept && !loading && (
          <div style={{ textAlign: "center", marginBottom: "2rem" }}>
            <div style={{ width: "3rem", height: "3rem", background: "rgba(196,152,90,0.1)", border: "1px solid rgba(196,152,90,0.25)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 1rem" }}>
              <Sparkles style={{ width: "1.4rem", height: "1.4rem", color: "var(--gold)" }} />
            </div>
            <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "2rem", color: "var(--cream-0)", marginBottom: "0.4rem", lineHeight: 1.1 }}>
              Deep Dive<span style={{ color: "var(--gold)" }}>.</span>
            </h1>
            <p style={{ ...body, fontSize: "1rem", color: "var(--cream-2)" }}>
              Search any concept for a full breakdown — equations, papers, videos, and a knowledge graph.
            </p>
          </div>
        )}

        {/* Search bar */}
        <div style={{ marginBottom: "1.5rem", position: "relative" }} ref={dropdownRef}>
          <div style={{ display: "flex", gap: "0.5rem" }}>
            <div style={{ flex: 1, position: "relative" }}>
              <Search style={{ position: "absolute", left: "0.75rem", top: "50%", transform: "translateY(-50%)", width: "0.9rem", height: "0.9rem", color: "var(--cream-2)", pointerEvents: "none", zIndex: 1 }} />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => { setQuery(e.target.value); setHighlightIdx(-1); setDropdownOpen(e.target.value.trim().length > 0); }}
                onKeyDown={handleKeyDown}
                onFocus={() => { if (query.trim()) setDropdownOpen(true); }}
                placeholder="Search for a concept..."
                disabled={loading}
                style={{ width: "100%", paddingLeft: "2.25rem", paddingRight: "1rem", paddingTop: "0.75rem", paddingBottom: "0.75rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.12)", outline: "none", ...body, fontSize: "0.95rem", color: "var(--cream-0)", boxSizing: "border-box", opacity: loading ? 0.6 : 1 }}
              />
              {dropdownOpen && filteredSuggestions.length > 0 && (
                <div style={{ position: "absolute", zIndex: 20, left: 0, right: 0, marginTop: "0.25rem", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.1)", maxHeight: "15rem", overflowY: "auto" }}>
                  {filteredSuggestions.slice(0, 10).map((s, idx) => {
                    const matchStart = s.label.toLowerCase().indexOf(query.toLowerCase().trim());
                    const matchEnd = matchStart + query.trim().length;
                    return (
                      <button key={s.label} onClick={() => handleSearch(s.label)} onMouseEnter={() => setHighlightIdx(idx)}
                        style={{ width: "100%", textAlign: "left", padding: "0.6rem 1rem", background: idx === highlightIdx ? "rgba(196,152,90,0.08)" : "none", border: "none", cursor: "pointer", display: "flex", alignItems: "center", gap: "0.5rem", ...body, fontSize: "0.9rem", color: "var(--cream-1)", borderBottom: "1px solid rgba(240,233,214,0.05)" }}>
                        <Search style={{ width: "0.75rem", height: "0.75rem", color: "var(--cream-2)", flexShrink: 0 }} />
                        <span>
                          {matchStart >= 0 ? (
                            <>{s.label.slice(0, matchStart)}<span style={{ fontWeight: 600, color: "var(--gold)" }}>{s.label.slice(matchStart, matchEnd)}</span>{s.label.slice(matchEnd)}</>
                          ) : s.label}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
            <button
              onClick={() => handleSearch()}
              disabled={!query.trim() || loading}
              style={{ background: !query.trim() || loading ? "rgba(196,152,90,0.3)" : "var(--gold)", border: "none", cursor: !query.trim() || loading ? "not-allowed" : "pointer", color: "var(--ink)", padding: "0 1rem", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transition: "background 0.2s" }}
            >
              {loading ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> : <Search style={{ width: "1rem", height: "1rem" }} />}
            </button>
          </div>
        </div>

        {/* Suggestion chips */}
        {!concept && !loading && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", justifyContent: "center", marginBottom: "2rem" }}>
            {suggestionsLoading ? (
              <span style={{ ...mono, fontSize: "0.55rem", color: "var(--cream-2)", letterSpacing: "0.1em" }}>Loading suggestions…</span>
            ) : (
              suggestions.slice(0, 20).map((s) => (
                <button key={s.label} onClick={() => handleSearch(s.label)}
                  style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.08em", textTransform: "uppercase", padding: "0.3rem 0.75rem", background: "none", border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", color: "var(--cream-2)", transition: "border-color 0.15s, color 0.15s" }}
                  onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.35)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--gold)"; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.1)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}
                >
                  {s.label}
                </button>
              ))
            )}
          </div>
        )}

        {/* Back button */}
        {concept && !loading && (
          <button onClick={() => { setConcept(null); setQuery(""); }}
            style={{ display: "flex", alignItems: "center", gap: "0.375rem", background: "none", border: "none", cursor: "pointer", ...mono, fontSize: "0.55rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "1rem", transition: "color 0.2s" }}
            onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
            onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}
          >
            <ArrowLeft style={{ width: "0.75rem", height: "0.75rem" }} /> Back to search
          </button>
        )}

        {/* Loading */}
        {loading && (
          <div style={{ textAlign: "center", padding: "5rem 0" }}>
            <Loader2 style={{ width: "2rem", height: "2rem", color: "var(--gold)", margin: "0 auto 1rem" }} className="animate-spin" />
            <p style={{ ...mono, fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>
              Generating deep dive — finding papers, equations, and videos…
            </p>
          </div>
        )}

        {error && !loading && (
          <div style={{ textAlign: "center", padding: "3rem 0" }}>
            <p style={{ ...mono, fontSize: "0.6rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--rose)", marginBottom: "0.5rem" }}>Unavailable</p>
            <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-2)" }}>{error}</p>
          </div>
        )}

        {concept && !loading && (
          <ConceptPageView concept={concept} onRelatedClick={handleRelatedClick} />
        )}
      </div>
    </div>
  );
}

function ConceptPageView({ concept, onRelatedClick }: { concept: ConceptPageResponse; onRelatedClick: (topic: string) => void }) {
  let idx = 0;

  return (
    <div key={concept.id} style={{ paddingBottom: "3rem" }}>
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(10px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      {/* Header */}
      <RevealSection index={idx++}>
        <div style={{ ...card }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "1rem" }}>
            <div>
              <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "1.75rem", color: "var(--cream-0)", marginBottom: "0.5rem", lineHeight: 1.1 }}>{concept.topic}</h1>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
                <LevelBadge level={concept.level} />
                {concept.prerequisites.length > 0 && (
                  <div style={{ display: "flex", alignItems: "center", gap: "0.25rem", ...mono, fontSize: "0.55rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>
                    <ChevronRight style={{ width: "0.65rem", height: "0.65rem" }} />
                    <span>Requires: </span>
                    {concept.prerequisites.slice(0, 3).map((p, i) => (
                      <button key={i} onClick={() => onRelatedClick(p)}
                        style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-1)", textDecoration: "underline", textUnderlineOffset: "2px", ...mono, fontSize: "0.55rem", transition: "color 0.15s" }}
                        onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--gold)"}
                        onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
                      >
                        {p}{i < Math.min(concept.prerequisites.length, 3) - 1 ? "," : ""}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <Sparkles style={{ width: "1rem", height: "1rem", color: "rgba(196,152,90,0.3)", flexShrink: 0, marginTop: "0.25rem" }} />
          </div>
        </div>
      </RevealSection>

      {/* Simple definition */}
      <RevealSection index={idx++}>
        <div style={card}>
          <div style={sectionLabel}>Simple Definition</div>
          <p style={{ ...body, fontSize: "0.95rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.75 }}>{concept.simple_definition}</p>
        </div>
      </RevealSection>

      {/* Why it matters */}
      <RevealSection index={idx++}>
        <div style={card}>
          <div style={sectionTitle}><Star style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Why It Matters</div>
          <p style={{ ...body, fontSize: "0.95rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.75, whiteSpace: "pre-line" }}>{concept.why_it_matters}</p>
        </div>
      </RevealSection>

      {/* Key equations */}
      {concept.key_equations.length > 0 && (
        <RevealSection index={idx++}>
          <div style={{ ...card, border: "1px solid rgba(129,140,248,0.2)", background: "rgba(99,102,241,0.04)" }}>
            <div style={sectionTitle}><Sigma style={{ width: "0.7rem", height: "0.7rem", color: "#818cf8" }} /> Key Equations</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {concept.key_equations.map((eq: KeyEquation, i: number) => (
                <div key={i} style={{ border: "1px solid rgba(129,140,248,0.15)", background: "rgba(15,15,20,0.6)", padding: "1rem" }}>
                  <div style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "#818cf8", marginBottom: "0.5rem" }}>{eq.label}</div>
                  <code style={{ display: "block", fontFamily: "monospace", fontSize: "0.85rem", color: "var(--cream-0)", background: "rgba(240,233,214,0.04)", padding: "0.5rem 0.75rem", marginBottom: "0.5rem", overflowX: "auto" }}>{eq.latex}</code>
                  <p style={{ ...body, fontSize: "0.85rem", color: "var(--cream-2)", lineHeight: 1.6 }}>{eq.description}</p>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Detailed explanation */}
      <RevealSection index={idx++}>
        <div style={card}>
          <div style={sectionTitle}><BookMarked style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Detailed Explanation</div>
          <div style={{ ...body, fontSize: "0.95rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.75, whiteSpace: "pre-line" }}>{concept.detailed_explanation}</div>
        </div>
      </RevealSection>

      {/* Analogy */}
      <RevealSection index={idx++}>
        <div style={{ ...card, border: "1px solid rgba(196,152,90,0.2)", background: "rgba(196,152,90,0.04)" }}>
          <div style={{ ...sectionLabel, color: "var(--gold)" }}>Analogy</div>
          <p style={{ ...body, fontSize: "0.95rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.75 }}>{concept.analogy}</p>
        </div>
      </RevealSection>

      {/* Real-world example */}
      <RevealSection index={idx++}>
        <div style={card}>
          <div style={sectionTitle}><Lightbulb style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Real-World Example</div>
          <div style={{ ...body, fontSize: "0.9rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.7, whiteSpace: "pre-line", fontFamily: "monospace", background: "rgba(240,233,214,0.03)", padding: "1rem", border: "1px solid rgba(240,233,214,0.06)" }}>{concept.real_world_example}</div>
        </div>
      </RevealSection>

      {/* Misconceptions */}
      {concept.misconceptions.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><AlertTriangle style={{ width: "0.7rem", height: "0.7rem", color: "#f97316" }} /> Common Misconceptions</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {concept.misconceptions.map((m, i) => (
                <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "0.75rem", padding: "0.75rem 1rem", background: m.is_correct ? "rgba(107,153,118,0.06)" : "rgba(239,68,68,0.05)", border: m.is_correct ? "1px solid rgba(107,153,118,0.2)" : "1px solid rgba(239,68,68,0.15)" }}>
                  {m.is_correct
                    ? <CheckCircle2 style={{ width: "0.9rem", height: "0.9rem", color: "var(--sage-c)", flexShrink: 0, marginTop: "0.15rem" }} />
                    : <XCircle style={{ width: "0.9rem", height: "0.9rem", color: "#ef4444", flexShrink: 0, marginTop: "0.15rem" }} />
                  }
                  <span style={{ ...body, fontSize: "0.9rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.6 }}>{m.text}</span>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Key takeaways */}
      {concept.key_takeaways.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><Star style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Key Takeaways</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              {concept.key_takeaways.map((t, i) => (
                <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "0.6rem" }}>
                  <CheckCircle2 style={{ width: "0.85rem", height: "0.85rem", color: "var(--gold)", flexShrink: 0, marginTop: "0.2rem" }} />
                  <span style={{ ...body, fontSize: "0.9rem", color: "rgba(210,208,220,0.88)", lineHeight: 1.65 }}>{t}</span>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Papers */}
      {concept.papers.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><FlaskConical style={{ width: "0.7rem", height: "0.7rem", color: "#a78bfa" }} /> Key Papers</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {concept.papers.map((p: ConceptPaper, i: number) => {
                const searchQuery = encodeURIComponent(`${p.title} ${p.authors} ${p.year}`);
                const scholarUrl = `https://scholar.google.com/scholar?q=${searchQuery}`;
                return (
                  <a key={i} href={scholarUrl} target="_blank" rel="noopener noreferrer"
                    style={{ display: "flex", alignItems: "flex-start", gap: "0.75rem", padding: "0.75rem", border: "1px solid rgba(167,139,250,0.12)", background: "none", textDecoration: "none", transition: "border-color 0.15s, background 0.15s" }}
                    onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(167,139,250,0.3)"; (e.currentTarget as HTMLAnchorElement).style.background = "rgba(167,139,250,0.04)"; }}
                    onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(167,139,250,0.12)"; (e.currentTarget as HTMLAnchorElement).style.background = "none"; }}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "0.25rem", ...body, fontSize: "0.9rem", fontWeight: 500, color: "var(--cream-0)", marginBottom: "0.2rem" }}>
                        {p.title} <ExternalLink style={{ width: "0.65rem", height: "0.65rem", opacity: 0.5, flexShrink: 0 }} />
                      </div>
                      <p style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.08em", color: "var(--cream-2)", marginBottom: "0.3rem" }}>{p.authors} · {p.year}</p>
                      <p style={{ ...body, fontSize: "0.82rem", color: "var(--cream-2)", lineHeight: 1.55 }}>{p.description}</p>
                    </div>
                  </a>
                );
              })}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Videos */}
      {concept.videos.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><Youtube style={{ width: "0.7rem", height: "0.7rem", color: "#ef4444" }} /> Recommended Videos</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              {concept.videos.map((v: ConceptVideo, i: number) => {
                const ytUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(v.search_query)}`;
                return (
                  <a key={i} href={ytUrl} target="_blank" rel="noopener noreferrer"
                    style={{ display: "flex", alignItems: "center", gap: "0.75rem", padding: "0.65rem 0.75rem", border: "1px solid rgba(239,68,68,0.12)", textDecoration: "none", transition: "border-color 0.15s, background 0.15s" }}
                    onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(239,68,68,0.3)"; (e.currentTarget as HTMLAnchorElement).style.background = "rgba(239,68,68,0.04)"; }}
                    onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(239,68,68,0.12)"; (e.currentTarget as HTMLAnchorElement).style.background = "none"; }}
                  >
                    <div style={{ width: "2rem", height: "2rem", background: "rgba(239,68,68,0.1)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                      <Youtube style={{ width: "0.9rem", height: "0.9rem", color: "#ef4444" }} />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-0)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{v.title}</p>
                      <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>{v.channel}</p>
                    </div>
                    <ExternalLink style={{ width: "0.75rem", height: "0.75rem", color: "var(--cream-2)", flexShrink: 0 }} />
                  </a>
                );
              })}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Knowledge Graph */}
      {concept.related_concepts.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><Network style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Knowledge Graph</div>
            <ConceptWeb center={concept.topic} nodes={concept.related_concepts} onNodeClick={onRelatedClick} />
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", marginTop: "0.75rem" }}>
              {concept.related_concepts.map((rc) => (
                <button key={rc} onClick={() => onRelatedClick(rc)}
                  style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.08em", textTransform: "uppercase", padding: "0.3rem 0.65rem", background: "none", border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", color: "var(--cream-2)", display: "flex", alignItems: "center", gap: "0.3rem", transition: "border-color 0.15s, color 0.15s" }}
                  onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(196,152,90,0.35)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--gold)"; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(240,233,214,0.1)"; (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"; }}
                >
                  {rc} <ArrowRight style={{ width: "0.6rem", height: "0.6rem" }} />
                </button>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Further reading */}
      {concept.further_reading.length > 0 && (
        <RevealSection index={idx++}>
          <div style={card}>
            <div style={sectionTitle}><GraduationCap style={{ width: "0.7rem", height: "0.7rem", color: "var(--gold)" }} /> Further Reading</div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              {concept.further_reading.map((fr, i) => (
                <li key={i} style={{ display: "flex", alignItems: "flex-start", gap: "0.5rem" }}>
                  <Link2 style={{ width: "0.75rem", height: "0.75rem", color: "var(--gold)", flexShrink: 0, marginTop: "0.2rem" }} />
                  <span style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", lineHeight: 1.6 }}>{fr}</span>
                </li>
              ))}
            </ul>
          </div>
        </RevealSection>
      )}
    </div>
  );
}
