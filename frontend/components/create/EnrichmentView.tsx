"use client";
import { useState, useRef, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Loader2,
  CheckCircle2,
  Search,
  Zap,
  Download,
  ExternalLink,
  FileText,
  PackageCheck,
  Square,
  ChevronDown,
  ChevronRight,
  XCircle,
  Plus,
  Play,
  ArrowLeft,
} from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { EnrichmentEvent } from "@/lib/useCreatorState";

interface EnrichmentViewProps {
  state: ReturnType<typeof useCreatorState>;
}

interface SourcePick {
  url: string;
  title: string;
  role?: string;
  why?: string;
  gaps_covered?: string[];
  level?: string;
}

interface NearMiss {
  url: string;
  title: string;
  why_not?: string;
}

interface LessonEnrichment {
  slug: string;
  title: string;
  topic?: string;
  status: "searching" | "curating" | "downloading" | "referencing" | "done";
  picks: SourcePick[];
  nearMisses: NearMiss[];
  queryCount: number;
  citationCount: number;
  downloadsSaved: number;
  downloadsSkipped: number;
  refDownloads: number;
}

function buildLessonEnrichments(events: EnrichmentEvent[]): Map<string, LessonEnrichment> {
  const map = new Map<string, LessonEnrichment>();

  for (const ev of events) {
    const slug = ev.slug;
    if (!slug) continue;

    if (!map.has(slug)) {
      map.set(slug, {
        slug,
        title: (ev.data.title as string) || slug,
        status: "searching",
        picks: [],
        nearMisses: [],
        queryCount: 0,
        citationCount: 0,
        downloadsSaved: 0,
        downloadsSkipped: 0,
        refDownloads: 0,
      });
    }
    const lesson = map.get(slug)!;

    switch (ev.type) {
      case "queries":
        lesson.queryCount = (ev.data.queries as string[])?.length || 0;
        lesson.status = "searching";
        break;
      case "search_result":
        lesson.citationCount = (ev.data.citation_count as number) || 0;
        lesson.status = "curating";
        break;
      case "curation":
        lesson.title = (ev.data.title as string) || lesson.title;
        lesson.topic = (ev.data.topic as string) || lesson.topic;
        lesson.picks = ((ev.data.picks as SourcePick[]) || []).map((p) => ({
          url: p.url || "",
          title: p.title || "",
          role: p.role || "",
          why: p.why || "",
          gaps_covered: p.gaps_covered || [],
          level: p.level || "",
        }));
        lesson.nearMisses = ((ev.data.near_misses as NearMiss[]) || []).map((nm) => ({
          url: nm.url || "",
          title: nm.title || "",
          why_not: nm.why_not || "",
        }));
        lesson.status = "downloading";
        break;
      case "download":
        lesson.downloadsSaved = (ev.data.saved as number) || 0;
        lesson.downloadsSkipped = (ev.data.skipped as number) || 0;
        lesson.topic = (ev.data.topic as string) || lesson.topic;
        lesson.status = "referencing";
        break;
      case "reference_enrichment":
        lesson.refDownloads = (ev.data.downloads as number) || 0;
        lesson.status = "done";
        break;
    }
  }

  return map;
}

export function EnrichmentView({ state }: EnrichmentViewProps) {
  const {
    enriching,
    enrichmentLog,
    cancelEnrichment,
    generateContent,
    generating,
    assessingCoverage,
    setActiveView,
    outline,
  } = state;
  const [showRawLog, setShowRawLog] = useState(false);
  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedSlugs, setSelectedSlugs] = useState<Set<string>>(new Set());

  const allSlugs = outline
    ? outline.modules.flatMap((m) => m.lessons.map((l) => l.slug))
    : [];
  const allLessons = outline
    ? outline.modules.flatMap((m) => m.lessons)
    : [];

  const toggleSlug = (slug: string) => {
    setSelectedSlugs((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  };

  const startBuildSelected = () => {
    if (selectedSlugs.size > 0) {
      generateContent(false, Array.from(selectedSlugs));
      setSelectionMode(false);
    }
  };

  if (enrichmentLog.length === 0 && !enriching) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-muted-foreground px-8 text-center">
        <Zap className="h-8 w-8 opacity-40" />
        <div className="space-y-1">
          <p className="text-sm font-medium">No enrichment activity yet</p>
          <p className="text-xs">
            Click &quot;Enrich&quot; in the Research tab to search for sources
            and expand the knowledge base for thin or missing concepts.
          </p>
        </div>
      </div>
    );
  }

  const lessonMap = buildLessonEnrichments(enrichmentLog);
  const stats = computeStats(enrichmentLog, lessonMap);
  const lessonEntries = Array.from(lessonMap.values());

  return (
    <div className="flex flex-col flex-1 min-h-0">
      {/* Header with live stats */}
      <div className="p-4 pb-3 border-b border-border shrink-0 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold flex items-center gap-2">
            {enriching ? (
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
            ) : (
              <PackageCheck className="h-4 w-4 text-green-500" />
            )}
            {enriching ? "Enrichment in progress..." : "Enrichment complete"}
          </h2>
          <div className="flex items-center gap-2">
            {enriching && (
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5 text-xs h-7 text-destructive hover:text-destructive"
                onClick={cancelEnrichment}
              >
                <Square className="h-3 w-3 fill-current" />
                Stop
              </Button>
            )}
            <Badge variant="secondary" className="text-xs tabular-nums">
              {lessonEntries.length} lesson{lessonEntries.length !== 1 ? "s" : ""}
            </Badge>
          </div>
        </div>

        {/* Stats row */}
        <div className="flex items-center gap-4 text-xs flex-wrap">
          {stats.queries > 0 && (
            <span className="flex items-center gap-1.5 text-blue-500">
              <Search className="h-3 w-3" />
              {stats.queries} queries
            </span>
          )}
          {stats.searchResults > 0 && (
            <span className="flex items-center gap-1.5 text-cyan-500">
              <ExternalLink className="h-3 w-3" />
              {stats.searchResults} results
            </span>
          )}
          {stats.picks > 0 && (
            <span className="flex items-center gap-1.5 text-green-500">
              <CheckCircle2 className="h-3 w-3" />
              {stats.picks} picked
            </span>
          )}
          {stats.downloads > 0 && (
            <span className="flex items-center gap-1.5 text-emerald-500">
              <Download className="h-3 w-3" />
              {stats.downloads} downloaded
            </span>
          )}
        </div>

        {/* Progress bar */}
        {enriching && stats.totalLessons > 0 && (
          <div className="space-y-1">
            <div className="flex h-1.5 rounded-full overflow-hidden bg-muted">
              <div
                className="bg-primary transition-all duration-500 rounded-full"
                style={{
                  width: `${Math.max(5, (stats.completedLessons / stats.totalLessons) * 100)}%`,
                }}
              />
            </div>
            <p className="text-[10px] text-muted-foreground">
              {stats.completedLessons} of {stats.totalLessons} lessons processed
            </p>
          </div>
        )}

        {/* Next steps after enrichment */}
        {!enriching && enrichmentLog.length > 0 && !selectionMode && (
          <div className="flex items-center gap-2 pt-1">
            <Button
              variant="default"
              size="sm"
              className="gap-1.5 text-xs h-8"
              onClick={() => generateContent()}
              disabled={generating || assessingCoverage}
            >
              <Play className="h-3.5 w-3.5" />
              Build All ({allSlugs.length})
            </Button>
            {allSlugs.length > 1 && !generating && (
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5 text-xs h-8"
                onClick={() => {
                  setSelectedSlugs(new Set(allSlugs));
                  setSelectionMode(true);
                }}
              >
                Build Select...
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              className="gap-1.5 text-xs h-8"
              onClick={() => setActiveView("research")}
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Research
            </Button>
          </div>
        )}

        {/* Build selection mode */}
        {selectionMode && (
          <div className="space-y-2 pt-1">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">
                Select lessons to build ({selectedSlugs.size} of {allSlugs.length})
              </p>
              <div className="flex items-center gap-1.5">
                <Button
                  variant="default"
                  size="sm"
                  className="gap-1.5 text-xs h-7"
                  onClick={startBuildSelected}
                  disabled={selectedSlugs.size === 0 || generating}
                >
                  <Play className="h-3 w-3" />
                  Build {selectedSlugs.size}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-xs h-7"
                  onClick={() => setSelectionMode(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-1 max-h-32 overflow-y-auto">
              {allLessons.map((l) => (
                <label
                  key={l.slug}
                  className="flex items-center gap-2 text-xs cursor-pointer hover:bg-muted/50 rounded px-2 py-1"
                >
                  <input
                    type="checkbox"
                    checked={selectedSlugs.has(l.slug)}
                    onChange={() => toggleSlug(l.slug)}
                    className="rounded border-border"
                  />
                  <span className="truncate">{l.title}</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Per-lesson cards */}
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-4 space-y-2">
          {lessonEntries.map((lesson) => (
            <LessonEnrichmentCard
              key={lesson.slug}
              lesson={lesson}
              onPromote={state}
            />
          ))}

          {/* Collapsible raw log */}
          <button
            onClick={() => setShowRawLog(!showRawLog)}
            className="flex items-center gap-1.5 w-full text-xs text-muted-foreground hover:text-foreground py-2 transition-colors"
          >
            {showRawLog ? (
              <ChevronDown className="h-3 w-3" />
            ) : (
              <ChevronRight className="h-3 w-3" />
            )}
            Raw event log ({enrichmentLog.length} events)
          </button>

          {showRawLog && (
            <RawEventLog events={enrichmentLog} active={enriching} />
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

/* ── Per-lesson enrichment card ────────────────────── */

function LessonEnrichmentCard({
  lesson,
  onPromote,
}: {
  lesson: LessonEnrichment;
  onPromote: ReturnType<typeof useCreatorState>;
}) {
  const [expanded, setExpanded] = useState(lesson.status !== "done");

  const statusConfig = {
    searching: { icon: Search, color: "text-blue-500", label: "Searching..." },
    curating: { icon: FileText, color: "text-purple-500", label: "Curating..." },
    downloading: { icon: Download, color: "text-emerald-500", label: "Downloading..." },
    referencing: { icon: FileText, color: "text-indigo-500", label: "References..." },
    done: { icon: CheckCircle2, color: "text-green-500", label: "Complete" },
  };

  const cfg = statusConfig[lesson.status];
  const StatusIcon = cfg.icon;

  return (
    <Card className="overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-3 w-full px-4 py-3 text-left hover:bg-accent/20 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        ) : (
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        )}
        <StatusIcon
          className={`h-4 w-4 shrink-0 ${cfg.color} ${
            lesson.status !== "done" ? "animate-pulse" : ""
          }`}
        />
        <span className="text-sm font-medium flex-1 truncate">{lesson.title}</span>
        <div className="flex items-center gap-2 shrink-0">
          {lesson.picks.length > 0 && (
            <span className="text-xs text-green-500 flex items-center gap-1">
              <CheckCircle2 className="h-3 w-3" />
              {lesson.picks.length}
            </span>
          )}
          {lesson.nearMisses.length > 0 && (
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <XCircle className="h-3 w-3" />
              {lesson.nearMisses.length}
            </span>
          )}
          <Badge
            variant="secondary"
            className={`text-[10px] ${lesson.status === "done" ? "bg-green-500/15 text-green-500" : ""}`}
          >
            {cfg.label}
          </Badge>
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-1 border-t border-border/50 space-y-3">
          {/* Picks */}
          {lesson.picks.length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Sources Picked ({lesson.picks.length})
              </p>
              <div className="space-y-1.5">
                {lesson.picks.map((pick) => (
                  <SourcePickRow key={pick.url} pick={pick} />
                ))}
              </div>
            </div>
          )}

          {/* Near misses */}
          {lesson.nearMisses.length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Skipped ({lesson.nearMisses.length})
              </p>
              <div className="space-y-1.5">
                {lesson.nearMisses.map((nm) => (
                  <NearMissRow
                    key={nm.url}
                    nearMiss={nm}
                    topicSlug={lesson.topic}
                    state={onPromote}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Stats summary */}
          {(lesson.queryCount > 0 || lesson.downloadsSaved > 0) && (
            <div className="flex items-center gap-3 text-[10px] text-muted-foreground pt-1">
              {lesson.queryCount > 0 && (
                <span>{lesson.queryCount} queries</span>
              )}
              {lesson.citationCount > 0 && (
                <span>{lesson.citationCount} citations</span>
              )}
              {lesson.downloadsSaved > 0 && (
                <span>{lesson.downloadsSaved} downloaded</span>
              )}
              {lesson.downloadsSkipped > 0 && (
                <span>{lesson.downloadsSkipped} skipped</span>
              )}
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

/* ── Source pick row ────────────────────────────────── */

function SourcePickRow({ pick }: { pick: SourcePick }) {
  return (
    <div className="flex items-start gap-2 text-xs">
      <CheckCircle2 className="h-3.5 w-3.5 text-green-500 shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">
        <a
          href={pick.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium hover:underline truncate block"
        >
          {pick.title || pick.url}
        </a>
        <div className="flex items-center gap-2 mt-0.5">
          {pick.role && (
            <Badge variant="outline" className="text-[9px] px-1 py-0">
              {pick.role}
            </Badge>
          )}
          {pick.level && (
            <Badge variant="outline" className="text-[9px] px-1 py-0">
              {pick.level}
            </Badge>
          )}
        </div>
        {pick.why && (
          <p className="text-muted-foreground mt-0.5 leading-relaxed">{pick.why}</p>
        )}
      </div>
    </div>
  );
}

/* ── Near miss row (with Keep button) ──────────────── */

function NearMissRow({
  nearMiss,
  topicSlug,
  state,
}: {
  nearMiss: NearMiss;
  topicSlug?: string;
  state: ReturnType<typeof useCreatorState>;
}) {
  const [promoting, setPromoting] = useState(false);
  const [promoted, setPromoted] = useState(false);

  const handlePromote = async () => {
    if (!topicSlug || !nearMiss.url) return;
    setPromoting(true);
    try {
      const { promoteSource } = state;
      if (promoteSource) {
        await promoteSource(topicSlug, nearMiss.url, nearMiss.title);
        setPromoted(true);
      }
    } catch (err) {
      console.error("Failed to promote source:", err);
    } finally {
      setPromoting(false);
    }
  };

  if (promoted) {
    return (
      <div className="flex items-start gap-2 text-xs">
        <CheckCircle2 className="h-3.5 w-3.5 text-green-500 shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <span className="font-medium text-green-500">
            {nearMiss.title || nearMiss.url}
          </span>
          <p className="text-muted-foreground mt-0.5">Added to wiki</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2 text-xs">
      <XCircle className="h-3.5 w-3.5 text-muted-foreground/50 shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">
        <a
          href={nearMiss.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-muted-foreground hover:underline hover:text-foreground truncate block"
        >
          {nearMiss.title || nearMiss.url}
        </a>
        {nearMiss.why_not && (
          <p className="text-muted-foreground/60 mt-0.5 leading-relaxed">{nearMiss.why_not}</p>
        )}
      </div>
      {topicSlug && nearMiss.url && (
        <Button
          variant="ghost"
          size="sm"
          className="text-[10px] h-6 px-2 gap-1 shrink-0"
          onClick={handlePromote}
          disabled={promoting}
        >
          {promoting ? (
            <Loader2 className="h-3 w-3 animate-spin" />
          ) : (
            <Plus className="h-3 w-3" />
          )}
          Keep
        </Button>
      )}
    </div>
  );
}

/* ── Stats helper ──────────────────────────────────── */

function computeStats(
  events: EnrichmentEvent[],
  lessonMap?: Map<string, LessonEnrichment>,
) {
  let queries = 0;
  let searchResults = 0;
  let picks = 0;
  let downloads = 0;
  let totalLessons = 0;

  for (const ev of events) {
    switch (ev.type) {
      case "assessment_summary":
        totalLessons =
          ((ev.data.needs_research as number) || 0) +
          ((ev.data.no_match as number) || 0);
        break;
      case "queries":
        queries += (ev.data.queries as string[])?.length || 0;
        break;
      case "search_result":
        searchResults += (ev.data.citation_count as number) || 0;
        break;
      case "curation":
        picks += (ev.data.picks as unknown[])?.length || 0;
        break;
      case "download":
        downloads += (ev.data.saved as number) || 0;
        break;
    }
  }

  let completedLessons = 0;
  if (lessonMap) {
    for (const lesson of lessonMap.values()) {
      if (lesson.status === "done") completedLessons++;
    }
  }

  return { queries, searchResults, picks, downloads, totalLessons, completedLessons };
}

/* ── Raw event log (collapsible) ───────────────────── */

const TYPE_CONFIG: Record<
  string,
  { icon: React.ComponentType<React.SVGProps<SVGSVGElement>>; color: string; label: string }
> = {
  status: { icon: Loader2, color: "text-muted-foreground", label: "Status" },
  assessment_summary: { icon: Search, color: "text-blue-500", label: "Assessment" },
  bootstrap: { icon: Zap, color: "text-purple-500", label: "Bootstrap" },
  queries: { icon: Search, color: "text-blue-500", label: "Queries" },
  search_result: { icon: ExternalLink, color: "text-cyan-500", label: "Search" },
  curation: { icon: CheckCircle2, color: "text-green-500", label: "Curation" },
  download: { icon: Download, color: "text-emerald-500", label: "Download" },
  reference_enrichment: { icon: FileText, color: "text-indigo-500", label: "Ref Track" },
  enrich_complete: { icon: CheckCircle2, color: "text-green-500", label: "Complete" },
  done: { icon: PackageCheck, color: "text-green-500", label: "Done" },
};

function formatEvent(ev: EnrichmentEvent): string {
  const d = ev.data;
  switch (ev.type) {
    case "status":
      return (d.message as string) || "Processing...";
    case "assessment_summary":
      return `${d.fully_covered} covered, ${d.needs_research} need research, ${d.no_match} no match`;
    case "bootstrap":
      return `Created topic "${d.topic_created}" for "${d.title}"`;
    case "queries":
      return `${(d.queries as string[])?.length || 0} queries for ${d.slug}`;
    case "search_result":
      return `${d.citation_count} citations found for ${d.slug}`;
    case "curation": {
      const p = (d.picks as unknown[])?.length || 0;
      const m = (d.near_misses as unknown[])?.length || 0;
      return `${p} picked, ${m} near-misses for "${d.title}"`;
    }
    case "download":
      return `${d.saved} saved, ${d.skipped} skipped → ${d.topic}`;
    case "reference_enrichment":
      return `${d.downloads} ref downloads for ${d.slug}`;
    case "enrich_complete":
      return `Done: ${d.total_picks} picks, ${d.total_downloads} downloads`;
    default:
      return JSON.stringify(d).slice(0, 120);
  }
}

function RawEventLog({
  events,
  active,
}: {
  events: EnrichmentEvent[];
  active: boolean;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [events.length]);

  return (
    <div
      ref={scrollRef}
      className="max-h-64 overflow-y-auto bg-muted/20 rounded-md font-mono text-[11px]"
    >
      {events.map((ev) => {
        const cfg = TYPE_CONFIG[ev.type] || TYPE_CONFIG.status;
        const Icon = cfg.icon;
        return (
          <div
            key={ev.id}
            className="flex items-start gap-2 px-3 py-1 hover:bg-accent/10 border-b border-border/10"
          >
            <Icon
              className={`h-3 w-3 mt-0.5 shrink-0 ${cfg.color} ${
                ev.type === "status" && active ? "animate-spin" : ""
              }`}
            />
            <Badge
              variant="outline"
              className={`text-[9px] px-1 py-0 shrink-0 ${cfg.color} border-current/20`}
            >
              {cfg.label}
            </Badge>
            <span className="text-muted-foreground flex-1 break-words">
              {formatEvent(ev)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
