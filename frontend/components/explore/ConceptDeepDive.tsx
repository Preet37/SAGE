"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, ConceptPageResponse, ConceptSuggestion, KeyEquation, ConceptPaper, ConceptVideo } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
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

function LevelBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    beginner: "bg-green-500/20 text-green-400 border-green-500/30",
    intermediate: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    advanced: "bg-red-500/20 text-red-400 border-red-500/30",
  };
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", colors[level] || colors.intermediate)}>
      {level.charAt(0).toUpperCase() + level.slice(1)}
    </span>
  );
}

function RevealSection({ index, children }: { index: number; children: React.ReactNode }) {
  return (
    <div
      className="animate-[fadeSlideIn_0.4s_ease-out_both]"
      style={{ animationDelay: `${index * 120}ms` }}
    >
      {children}
    </div>
  );
}

// Simple SVG concept web — nodes for related concepts around a center
function ConceptWeb({
  center,
  nodes,
  onNodeClick,
}: {
  center: string;
  nodes: string[];
  onNodeClick: (n: string) => void;
}) {
  const r = 120;
  const cx = 180;
  const cy = 160;
  const displayed = nodes.slice(0, 8);

  return (
    <svg viewBox="0 0 360 320" className="w-full max-h-72 select-none">
      {/* edges */}
      {displayed.map((_, i) => {
        const angle = (2 * Math.PI * i) / displayed.length - Math.PI / 2;
        const nx = cx + r * Math.cos(angle);
        const ny = cy + r * Math.sin(angle);
        return (
          <line
            key={i}
            x1={cx} y1={cy}
            x2={nx} y2={ny}
            stroke="currentColor"
            strokeOpacity={0.15}
            strokeWidth={1.5}
          />
        );
      })}
      {/* peripheral nodes */}
      {displayed.map((label, i) => {
        const angle = (2 * Math.PI * i) / displayed.length - Math.PI / 2;
        const nx = cx + r * Math.cos(angle);
        const ny = cy + r * Math.sin(angle);
        const words = label.split(" ");
        return (
          <g key={i} className="cursor-pointer" onClick={() => onNodeClick(label)}>
            <circle cx={nx} cy={ny} r={28} className="fill-card stroke-border" strokeWidth={1.5} />
            <circle cx={nx} cy={ny} r={28} className="fill-primary/5 hover:fill-primary/15 transition-colors" />
            {words.slice(0, 2).map((word, wi) => (
              <text
                key={wi}
                x={nx}
                y={ny + (words.length > 1 ? (wi - 0.5) * 11 : 4)}
                textAnchor="middle"
                fontSize={8}
                className="fill-foreground font-medium"
              >
                {word.length > 10 ? word.slice(0, 9) + "…" : word}
              </text>
            ))}
          </g>
        );
      })}
      {/* center node */}
      <circle cx={cx} cy={cy} r={36} className="fill-primary/20 stroke-primary/60" strokeWidth={2} />
      {center.split(" ").slice(0, 3).map((word, i, arr) => (
        <text
          key={i}
          x={cx}
          y={cy + (i - (arr.length - 1) / 2) * 12 + 4}
          textAnchor="middle"
          fontSize={9}
          fontWeight="600"
          className="fill-primary"
        >
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
  const [suggestionsLoading, setSuggestionsLoading] = useState(true);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [highlightIdx, setHighlightIdx] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    api.concepts.getSuggestions(token)
      .then(setSuggestions)
      .catch(() => {})
      .finally(() => setSuggestionsLoading(false));
  }, [router]);

  useEffect(() => {
    if (initialQuery) {
      handleSearch(initialQuery);
    }
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
    try {
      const result = await api.concepts.search(searchTopic, token);
      setConcept(result);
    } catch (err) {
      console.error("Concept search failed:", err);
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

  function handleRelatedClick(topic: string) {
    setQuery(topic);
    handleSearch(topic);
  }

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) setDropdownOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="flex-1 overflow-y-auto min-h-0">
      <div className="max-w-3xl mx-auto px-6 py-8">
        {!concept && !loading && (
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-6 w-6 text-primary" />
            </div>
            <h1 className="text-2xl font-bold mb-2">Deep Dive</h1>
            <p className="text-muted-foreground text-sm">
              Search any concept for a full breakdown — equations, papers, videos, and a knowledge graph.
            </p>
          </div>
        )}

        {/* Search bar */}
        <div className="mb-6" ref={dropdownRef}>
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground z-10" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => { setQuery(e.target.value); setHighlightIdx(-1); setDropdownOpen(e.target.value.trim().length > 0); }}
                onKeyDown={handleKeyDown}
                onFocus={() => { if (query.trim()) setDropdownOpen(true); }}
                placeholder="Search for a concept..."
                disabled={loading}
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-border bg-background text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
              />
              {dropdownOpen && filteredSuggestions.length > 0 && (
                <div className="absolute z-20 left-0 right-0 mt-1 rounded-xl border border-border bg-popover shadow-lg max-h-60 overflow-y-auto">
                  {filteredSuggestions.slice(0, 10).map((s, idx) => {
                    const matchStart = s.label.toLowerCase().indexOf(query.toLowerCase().trim());
                    const matchEnd = matchStart + query.trim().length;
                    return (
                      <button
                        key={s.label}
                        onClick={() => handleSearch(s.label)}
                        onMouseEnter={() => setHighlightIdx(idx)}
                        className={cn(
                          "w-full text-left px-4 py-2.5 text-sm transition-colors flex items-center gap-2 first:rounded-t-xl last:rounded-b-xl",
                          idx === highlightIdx ? "bg-accent text-accent-foreground" : "hover:bg-accent/50"
                        )}
                      >
                        <Search className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                        <span>
                          {matchStart >= 0 ? (
                            <>{s.label.slice(0, matchStart)}<span className="font-semibold text-primary">{s.label.slice(matchStart, matchEnd)}</span>{s.label.slice(matchEnd)}</>
                          ) : s.label}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
            <Button onClick={() => handleSearch()} disabled={!query.trim() || loading} size="icon" className="h-[46px] w-[46px] rounded-xl flex-shrink-0">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        {/* Suggestion chips */}
        {!concept && !loading && (
          <div className="flex flex-wrap gap-2 justify-center mb-8">
            {suggestionsLoading ? (
              <span className="text-sm text-muted-foreground">Loading suggestions...</span>
            ) : (
              suggestions.slice(0, 20).map((s) => (
                <button
                  key={s.label}
                  onClick={() => handleSearch(s.label)}
                  className="text-xs px-3 py-1.5 rounded-full border border-border bg-card/50 text-muted-foreground hover:text-foreground hover:border-primary/40 hover:bg-primary/5 transition-all"
                >
                  {s.label}
                </button>
              ))
            )}
          </div>
        )}

        {concept && !loading && (
          <button
            onClick={() => { setConcept(null); setQuery(""); }}
            className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors mb-4"
          >
            <ArrowLeft className="h-4 w-4" /> Back to search
          </button>
        )}

        {loading && (
          <div className="text-center py-20">
            <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
            <p className="text-sm text-muted-foreground">Generating deep dive — finding papers, equations, and videos...</p>
          </div>
        )}

        {concept && !loading && (
          <ConceptPageView concept={concept} onRelatedClick={handleRelatedClick} />
        )}
      </div>
    </div>
  );
}

function ConceptPageView({
  concept,
  onRelatedClick,
}: {
  concept: ConceptPageResponse;
  onRelatedClick: (topic: string) => void;
}) {
  let idx = 0;

  return (
    <div key={concept.id} className="space-y-5 pb-8">
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(10px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      {/* Header */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold mb-2">{concept.topic}</h1>
              <div className="flex items-center gap-2 flex-wrap">
                <LevelBadge level={concept.level} />
                {concept.prerequisites.length > 0 && (
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <ChevronRight className="h-3 w-3" />
                    <span>Requires: </span>
                    {concept.prerequisites.slice(0, 3).map((p, i) => (
                      <button
                        key={i}
                        onClick={() => onRelatedClick(p)}
                        className="underline underline-offset-2 hover:text-foreground transition-colors"
                      >
                        {p}{i < Math.min(concept.prerequisites.length, 3) - 1 ? "," : ""}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <Sparkles className="h-5 w-5 text-muted-foreground/30 flex-shrink-0 mt-1" />
          </div>
        </div>
      </RevealSection>

      {/* Simple definition */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-5">
          <div className="text-[10px] font-bold uppercase tracking-widest text-primary mb-3">Simple Definition</div>
          <p className="text-sm leading-relaxed">{concept.simple_definition}</p>
        </div>
      </RevealSection>

      {/* Why it matters */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-5">
          <h3 className="font-semibold mb-3 flex items-center gap-2 text-sm">
            <Star className="h-4 w-4 text-primary" /> Why It Matters
          </h3>
          <p className="text-sm leading-relaxed whitespace-pre-line">{concept.why_it_matters}</p>
        </div>
      </RevealSection>

      {/* Key equations */}
      {concept.key_equations.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/5 p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <Sigma className="h-4 w-4 text-indigo-400" /> Key Equations
            </h3>
            <div className="space-y-3">
              {concept.key_equations.map((eq: KeyEquation, i: number) => (
                <div key={i} className="rounded-lg border border-indigo-500/20 bg-background/60 p-4">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wide">{eq.label}</span>
                  </div>
                  <code className="block font-mono text-sm text-foreground bg-muted/50 rounded px-3 py-2 mb-2 overflow-x-auto">
                    {eq.latex}
                  </code>
                  <p className="text-xs text-muted-foreground leading-relaxed">{eq.description}</p>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Detailed explanation */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-5">
          <h3 className="font-semibold mb-3 flex items-center gap-2 text-sm">
            <BookMarked className="h-4 w-4 text-primary" /> Detailed Explanation
          </h3>
          <div className="text-sm leading-relaxed whitespace-pre-line">{concept.detailed_explanation}</div>
        </div>
      </RevealSection>

      {/* Analogy */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-5">
          <div className="text-[10px] font-bold uppercase tracking-widest text-amber-400 mb-3">Analogy</div>
          <p className="text-sm leading-relaxed">{concept.analogy}</p>
        </div>
      </RevealSection>

      {/* Real-world example */}
      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-5">
          <h3 className="font-semibold mb-3 flex items-center gap-2 text-sm">
            <Lightbulb className="h-4 w-4 text-primary" /> Real-World Example
          </h3>
          <div className="text-sm leading-relaxed whitespace-pre-line font-mono bg-muted/30 rounded-lg p-4">
            {concept.real_world_example}
          </div>
        </div>
      </RevealSection>

      {/* Misconceptions */}
      {concept.misconceptions.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <AlertTriangle className="h-4 w-4 text-orange-400" /> Common Misconceptions
            </h3>
            <div className="space-y-2">
              {concept.misconceptions.map((m, i) => (
                <div
                  key={i}
                  className={cn(
                    "flex items-start gap-3 px-4 py-3 rounded-lg text-sm",
                    m.is_correct ? "bg-green-500/5 border border-green-500/20" : "bg-red-500/5 border border-red-500/20"
                  )}
                >
                  {m.is_correct ? <CheckCircle2 className="h-4 w-4 text-green-400 flex-shrink-0 mt-0.5" /> : <XCircle className="h-4 w-4 text-red-400 flex-shrink-0 mt-0.5" />}
                  <span>{m.text}</span>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Key takeaways */}
      {concept.key_takeaways.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <Star className="h-4 w-4 text-primary" /> Key Takeaways
            </h3>
            <div className="space-y-2">
              {concept.key_takeaways.map((t, i) => (
                <div key={i} className="flex items-start gap-3 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-primary flex-shrink-0 mt-0.5" />
                  <span>{t}</span>
                </div>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Papers */}
      {concept.papers.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <FlaskConical className="h-4 w-4 text-violet-400" /> Key Papers
            </h3>
            <div className="space-y-3">
              {concept.papers.map((p: ConceptPaper, i: number) => {
                const searchQuery = encodeURIComponent(`${p.title} ${p.authors} ${p.year}`);
                const scholarUrl = `https://scholar.google.com/scholar?q=${searchQuery}`;
                return (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-lg border border-border hover:border-violet-500/30 hover:bg-violet-500/5 transition-all group">
                    <div className="flex-1 min-w-0">
                      <a
                        href={scholarUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium text-sm text-foreground group-hover:text-violet-400 transition-colors flex items-center gap-1"
                      >
                        {p.title}
                        <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 flex-shrink-0" />
                      </a>
                      <p className="text-xs text-muted-foreground mt-0.5">{p.authors} · {p.year}</p>
                      <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{p.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Videos */}
      {concept.videos.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <Youtube className="h-4 w-4 text-red-400" /> Recommended Videos
            </h3>
            <div className="space-y-2">
              {concept.videos.map((v: ConceptVideo, i: number) => {
                const ytUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(v.search_query)}`;
                return (
                  <a
                    key={i}
                    href={ytUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 rounded-lg border border-border hover:border-red-500/30 hover:bg-red-500/5 transition-all group"
                  >
                    <div className="w-8 h-8 rounded-lg bg-red-500/10 flex items-center justify-center flex-shrink-0">
                      <Youtube className="h-4 w-4 text-red-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground group-hover:text-red-400 transition-colors truncate">{v.title}</p>
                      <p className="text-xs text-muted-foreground">{v.channel}</p>
                    </div>
                    <ExternalLink className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 flex-shrink-0" />
                  </a>
                );
              })}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Concept knowledge graph */}
      {concept.related_concepts.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <Network className="h-4 w-4 text-primary" /> Knowledge Graph
            </h3>
            <ConceptWeb
              center={concept.topic}
              nodes={concept.related_concepts}
              onNodeClick={onRelatedClick}
            />
            <div className="flex flex-wrap gap-2 mt-3">
              {concept.related_concepts.map((rc) => (
                <button
                  key={rc}
                  onClick={() => onRelatedClick(rc)}
                  className="text-xs px-3 py-1.5 rounded-full border border-border bg-card text-muted-foreground hover:text-foreground hover:border-primary/40 hover:bg-primary/5 transition-all flex items-center gap-1"
                >
                  {rc} <ArrowRight className="h-3 w-3" />
                </button>
              ))}
            </div>
          </div>
        </RevealSection>
      )}

      {/* Further reading */}
      {concept.further_reading.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-sm">
              <GraduationCap className="h-4 w-4 text-primary" /> Further Reading
            </h3>
            <ul className="space-y-2">
              {concept.further_reading.map((fr, i) => (
                <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                  <Link2 className="h-3.5 w-3.5 text-primary flex-shrink-0 mt-0.5" />
                  <span>{fr}</span>
                </li>
              ))}
            </ul>
          </div>
        </RevealSection>
      )}
    </div>
  );
}
