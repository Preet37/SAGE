"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, ConceptPageResponse, ConceptSuggestion } from "@/lib/api";
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
      style={{ animationDelay: `${index * 800}ms` }}
    >
      {children}
    </div>
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

  // Auto-search if an initial query was provided
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
              Search any concept for a structured breakdown with examples, analogies, and misconceptions.
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

        {/* Back button */}
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
            <p className="text-sm text-muted-foreground">Generating concept page...</p>
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
    <div key={concept.id} className="space-y-6 pb-8">
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(12px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold mb-2">{concept.topic}</h1>
              <LevelBadge level={concept.level} />
            </div>
            <Sparkles className="h-6 w-6 text-muted-foreground/30" />
          </div>
        </div>
      </RevealSection>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <div className="text-[10px] font-bold uppercase tracking-widest text-primary mb-3">Simple Definition</div>
          <p className="text-sm leading-relaxed">{concept.simple_definition}</p>
        </div>
      </RevealSection>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <h3 className="font-semibold mb-3 flex items-center gap-2">
            <Star className="h-4 w-4 text-primary" /> Why It Matters
          </h3>
          <p className="text-sm leading-relaxed whitespace-pre-line">{concept.why_it_matters}</p>
        </div>
      </RevealSection>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <h3 className="font-semibold mb-3 flex items-center gap-2">
            <BookMarked className="h-4 w-4 text-primary" /> Detailed Explanation
          </h3>
          <div className="text-sm leading-relaxed whitespace-pre-line">{concept.detailed_explanation}</div>
        </div>
      </RevealSection>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-6">
          <div className="text-[10px] font-bold uppercase tracking-widest text-amber-400 mb-3">Analogy</div>
          <p className="text-sm leading-relaxed">{concept.analogy}</p>
        </div>
      </RevealSection>

      <RevealSection index={idx++}>
        <div className="rounded-xl border border-border bg-card p-6">
          <h3 className="font-semibold mb-3 flex items-center gap-2">
            <Lightbulb className="h-4 w-4 text-primary" /> Real-World Example
          </h3>
          <div className="text-sm leading-relaxed whitespace-pre-line font-mono bg-muted/30 rounded-lg p-4">
            {concept.real_world_example}
          </div>
        </div>
      </RevealSection>

      {concept.misconceptions.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
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

      {concept.key_takeaways.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
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

      {concept.related_concepts.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-6">
            <h3 className="font-semibold mb-4">Related Concepts</h3>
            <div className="flex flex-wrap gap-2">
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

      {concept.further_reading.length > 0 && (
        <RevealSection index={idx++}>
          <div className="rounded-xl border border-border bg-card p-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Link2 className="h-4 w-4 text-primary" /> Further Reading
            </h3>
            <ul className="space-y-2">
              {concept.further_reading.map((fr, i) => (
                <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
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
