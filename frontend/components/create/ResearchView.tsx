"use client";
import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Loader2,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ChevronDown,
  ChevronRight,
  Search,
  Zap,
  Play,
  RefreshCw,
  FileText,
} from "lucide-react";
import type { useCreatorState } from "@/lib/useCreatorState";
import type { LessonAssessment } from "@/lib/useCreatorState";

interface ResearchViewProps {
  state: ReturnType<typeof useCreatorState>;
}

export function ResearchView({ state }: ResearchViewProps) {
  const {
    coverageAssessment,
    assessingCoverage,
    enriching,
    enrichmentLog,
    phase,
    outline,
    assessCoverage,
    enrichCoverage,
    generateContent,
    generating,
    setActiveView,
  } = state;

  const [selectedSlugs, setSelectedSlugs] = useState<Set<string>>(new Set());
  const [selectionMode, setSelectionMode] = useState<"enrich" | "build" | null>(null);

  if (!coverageAssessment && !assessingCoverage && phase === "shaping") {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-muted-foreground px-8 text-center">
        <Search className="h-8 w-8 opacity-40" />
        <div className="space-y-1">
          <p className="text-sm font-medium">No coverage assessment yet</p>
          <p className="text-xs">
            Click &quot;Prepare Content&quot; in the Outline tab to assess wiki
            coverage for each lesson.
          </p>
        </div>
      </div>
    );
  }

  if (assessingCoverage && !coverageAssessment) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 text-muted-foreground">
        <Loader2 className="h-6 w-6 animate-spin" />
        <p className="text-sm">Assessing wiki coverage...</p>
        <p className="text-xs text-muted-foreground/60">
          Checking each lesson&apos;s concepts against the knowledge base
        </p>
      </div>
    );
  }

  if (!coverageAssessment) return null;

  const { lessons } = coverageAssessment;

  // Aggregate concept-level stats from all lessons
  let covered = 0, thin = 0, missing = 0;
  const allTopics = new Set<string>();
  let totalSources = 0;

  for (const lesson of lessons) {
    for (const val of Object.values(lesson.conceptVerdicts)) {
      const v = typeof val === "string" ? val : val?.verdict || "missing";
      if (v === "covered") covered++;
      else if (v === "thin") thin++;
      else missing++;
    }
    if (lesson.unmapped) missing += lesson.unmapped.length;
    for (const t of lesson.topics) allTopics.add(t);
    totalSources += lesson.sourceCount;
  }

  const totalConcepts = covered + thin + missing;
  const matched = covered + thin;
  const gaps = thin + missing;
  const coveragePct = totalConcepts > 0 ? Math.round((covered / totalConcepts) * 100) : 0;
  const matchedPct = totalConcepts > 0 ? Math.round((matched / totalConcepts) * 100) : 0;

  const sortedLessons = [...lessons].sort((a, b) => {
    const order = { no_match: 0, needs_research: 1, fully_covered: 2 };
    return order[a.verdict] - order[b.verdict];
  });

  const enrichableSlugs = lessons
    .filter((l) => l.verdict !== "fully_covered")
    .map((l) => l.slug);

  const allSlugs = lessons.map((l) => l.slug);

  const toggleSlug = (slug: string) => {
    setSelectedSlugs((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  };

  const startEnrichSelected = () => {
    const slugs = selectionMode === "enrich" && selectedSlugs.size > 0
      ? Array.from(selectedSlugs)
      : undefined;
    enrichCoverage(slugs);
    setSelectionMode(null);
  };

  const startBuildSelected = () => {
    if (selectedSlugs.size > 0) {
      generateContent(false, Array.from(selectedSlugs));
    }
    setSelectionMode(null);
  };

  const enterEnrichSelectionMode = () => {
    setSelectedSlugs(new Set(enrichableSlugs));
    setSelectionMode("enrich");
  };

  const enterBuildSelectionMode = () => {
    setSelectedSlugs(new Set(allSlugs));
    setSelectionMode("build");
  };

  return (
    <div className="flex flex-col flex-1 min-h-0">
      {/* Summary header */}
      <div className="p-6 pb-4 space-y-3 shrink-0 border-b border-border">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Knowledge Base Coverage</h2>
          <div className="flex items-center gap-2">
            {assessingCoverage && (
              <Badge variant="secondary" className="gap-1 text-xs">
                <Loader2 className="h-3 w-3 animate-spin" />
                Assessing...
              </Badge>
            )}
            {!assessingCoverage && !enriching && (
              <Button
                variant="ghost"
                size="sm"
                className="gap-1.5 text-xs h-7"
                onClick={assessCoverage}
              >
                <RefreshCw className="h-3 w-3" />
                Re-assess
              </Button>
            )}
          </div>
        </div>

        {/* Positive headline */}
        <p className="text-sm text-foreground">
          <span className="font-semibold">{matched} of {totalConcepts}</span> concepts matched
          {allTopics.size > 0 && (
            <span className="text-muted-foreground">
              {" "}across <span className="font-medium text-foreground">{allTopics.size}</span> wiki topic{allTopics.size !== 1 ? "s" : ""}
            </span>
          )}
          {totalSources > 0 && (
            <span className="text-muted-foreground">
              {" "}({totalSources} source{totalSources !== 1 ? "s" : ""} checked)
            </span>
          )}
        </p>

        {/* Segmented progress bar */}
        <div className="space-y-1.5">
          <div className="flex h-2.5 rounded-full overflow-hidden bg-muted">
            {covered > 0 && (
              <div
                className="bg-green-500 transition-all duration-500"
                style={{ width: `${(covered / totalConcepts) * 100}%` }}
              />
            )}
            {thin > 0 && (
              <div
                className="bg-amber-400 transition-all duration-500"
                style={{ width: `${(thin / totalConcepts) * 100}%` }}
              />
            )}
            {missing > 0 && (
              <div
                className="bg-red-400/60 transition-all duration-500"
                style={{ width: `${(missing / totalConcepts) * 100}%` }}
              />
            )}
          </div>
          <div className="flex items-center gap-4 text-xs">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-green-500 shrink-0" />
              {covered} covered
            </span>
            {thin > 0 && (
              <span className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-amber-400 shrink-0" />
                {thin} partial
              </span>
            )}
            {missing > 0 && (
              <span className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-red-400/60 shrink-0" />
                {missing} new
              </span>
            )}
          </div>
        </div>

        {/* Contextual enrichment CTA */}
        {!assessingCoverage && gaps > 0 && (
          <p className="text-xs text-muted-foreground">
            {thin > 0 && missing > 0
              ? `${thin} concept${thin !== 1 ? "s" : ""} need deeper coverage and ${missing} are new to the wiki.`
              : thin > 0
                ? `${thin} concept${thin !== 1 ? "s" : ""} need deeper coverage in the wiki.`
                : `${missing} concept${missing !== 1 ? "s" : ""} are new to the wiki.`}
            {" "}Enrich will search for sources and expand the knowledge base.
          </p>
        )}

        {/* Action buttons */}
        {!assessingCoverage && !selectionMode && (
          <div className="flex items-center gap-2 flex-wrap pt-1">
            {gaps > 0 && !enriching && (
              <>
                <Button
                  variant="default"
                  size="sm"
                  className="gap-1.5 text-xs h-8"
                  onClick={() => enrichCoverage()}
                >
                  <Zap className="h-3.5 w-3.5" />
                  Enrich All ({enrichableSlugs.length})
                </Button>
                {enrichableSlugs.length > 1 && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5 text-xs h-8"
                    onClick={enterEnrichSelectionMode}
                  >
                    Enrich Select...
                  </Button>
                )}
              </>
            )}
            {enriching && (
              <button
                onClick={() => setActiveView("enrichment")}
                className="inline-flex items-center gap-1.5 text-xs py-1 px-2 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
              >
                <Loader2 className="h-3 w-3 animate-spin" />
                Enriching... <span className="underline">View log</span>
              </button>
            )}
            <Button
              variant={gaps > 0 ? "outline" : "default"}
              size="sm"
              className="gap-1.5 text-xs h-8"
              onClick={() => generateContent()}
              disabled={generating || enriching || assessingCoverage}
            >
              <Play className="h-3.5 w-3.5" />
              Build All ({allSlugs.length})
            </Button>
            {allSlugs.length > 1 && !generating && !enriching && (
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5 text-xs h-8"
                onClick={enterBuildSelectionMode}
              >
                Build Select...
              </Button>
            )}
          </div>
        )}

        {/* Selection mode (enrich or build) */}
        {selectionMode && (
          <div className="flex items-center gap-2 pt-1">
            <Button
              variant="default"
              size="sm"
              className="gap-1.5 text-xs h-8"
              onClick={selectionMode === "enrich" ? startEnrichSelected : startBuildSelected}
              disabled={selectedSlugs.size === 0}
            >
              {selectionMode === "enrich" ? (
                <Zap className="h-3.5 w-3.5" />
              ) : (
                <Play className="h-3.5 w-3.5" />
              )}
              {selectionMode === "enrich" ? "Enrich" : "Build"} {selectedSlugs.size} Lesson{selectedSlugs.size !== 1 ? "s" : ""}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="text-xs h-8"
              onClick={() => setSelectionMode(null)}
            >
              Cancel
            </Button>
          </div>
        )}
      </div>

      {/* Lesson cards */}
      <ScrollArea className="flex-1 min-h-0">
        <div className="p-6 space-y-2">
          {selectionMode && (() => {
            const pool = selectionMode === "enrich" ? enrichableSlugs : allSlugs;
            return pool.length > 1 ? (
              <label className="flex items-center gap-2 px-4 py-2 text-xs text-muted-foreground cursor-pointer hover:text-foreground transition-colors">
                <input
                  type="checkbox"
                  checked={selectedSlugs.size === pool.length}
                  onChange={() =>
                    setSelectedSlugs(selectedSlugs.size === pool.length ? new Set() : new Set(pool))
                  }
                  className="rounded border-border"
                />
                {selectedSlugs.size === pool.length ? "Deselect all" : "Select all"}
              </label>
            ) : null;
          })()}
          {sortedLessons.map((lesson) => (
            <LessonAssessmentCard
              key={lesson.slug}
              lesson={lesson}
              selectionMode={selectionMode}
              selected={selectedSlugs.has(lesson.slug)}
              onToggle={() => toggleSlug(lesson.slug)}
            />
          ))}

          {/* Link to enrichment log if there's activity */}
          {enrichmentLog.length > 0 && !enriching && (
            <button
              onClick={() => setActiveView("enrichment")}
              className="w-full text-center text-xs text-muted-foreground hover:text-foreground py-3 transition-colors"
            >
              View enrichment log ({enrichmentLog.length} events) →
            </button>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

/* ── Lesson Assessment Card ─────────────────────────── */

function LessonAssessmentCard({
  lesson,
  selectionMode = null,
  selected = false,
  onToggle,
}: {
  lesson: LessonAssessment;
  selectionMode?: "enrich" | "build" | null;
  selected?: boolean;
  onToggle?: () => void;
}) {
  const [expanded, setExpanded] = useState(false);

  const verdictConfig = {
    fully_covered: {
      border: "border-l-green-500",
      bg: "bg-green-500/5",
      icon: CheckCircle2,
      iconColor: "text-green-400",
      label: "Covered",
      badgeCls: "bg-green-500/15 text-green-400",
    },
    needs_research: {
      border: "border-l-amber-500",
      bg: "bg-amber-500/5",
      icon: AlertTriangle,
      iconColor: "text-amber-400",
      label: "Partial",
      badgeCls: "bg-amber-500/15 text-amber-400",
    },
    no_match: {
      border: "border-l-red-500",
      bg: "bg-red-500/5",
      icon: XCircle,
      iconColor: "text-red-400",
      label: "New Topic",
      badgeCls: "bg-destructive/15 text-destructive",
    },
  };

  const config = verdictConfig[lesson.verdict];
  const Icon = config.icon;

  return (
    <Card
      className={`border-l-4 ${config.border} ${expanded ? config.bg : ""} overflow-hidden`}
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-3 w-full px-4 py-3 text-left hover:bg-accent/20 transition-colors"
      >
        {selectionMode && (selectionMode === "build" || lesson.verdict !== "fully_covered") ? (
          <input
            type="checkbox"
            checked={selected}
            onChange={(e) => {
              e.stopPropagation();
              onToggle?.();
            }}
            onClick={(e) => e.stopPropagation()}
            className="rounded border-border shrink-0"
          />
        ) : expanded ? (
          <ChevronDown className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        ) : (
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        )}
        <Icon className={`h-4 w-4 shrink-0 ${config.iconColor}`} />
        <span className="text-sm font-medium flex-1 truncate">
          {lesson.title}
        </span>
        <div className="flex items-center gap-2 shrink-0">
          {lesson.topics.length > 0 && (
            <span className="text-xs text-muted-foreground">
              {lesson.topics.length} topic{lesson.topics.length !== 1 ? "s" : ""}
            </span>
          )}
          {lesson.sourceCount > 0 && (
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <FileText className="h-3 w-3" />
              {lesson.sourceCount}
            </span>
          )}
          <Badge variant="secondary" className={`text-[10px] ${config.badgeCls}`}>
            {config.label}
          </Badge>
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-1 border-t border-border/50 space-y-3">
          {/* Topics */}
          {lesson.topics.length > 0 && (
            <div className="space-y-1">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Wiki Topics
              </p>
              <div className="flex flex-wrap gap-1">
                {lesson.topics.map((t) => (
                  <Badge key={t} variant="secondary" className="text-xs">
                    {t}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Concept verdicts */}
          {Object.keys(lesson.conceptVerdicts).length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Concept Coverage
              </p>
              <div className="grid gap-1">
                {Object.entries(lesson.conceptVerdicts).map(
                  ([concept, verdict]) => {
                    const v =
                      typeof verdict === "string"
                        ? verdict
                        : verdict?.verdict || "missing";
                    const explanation =
                      typeof verdict === "object" ? verdict?.explanation : undefined;
                    return (
                      <ConceptVerdictRow
                        key={concept}
                        concept={concept}
                        verdict={v as "covered" | "thin" | "missing"}
                        explanation={explanation}
                      />
                    );
                  },
                )}
              </div>
            </div>
          )}

          {/* Sources */}
          {lesson.sources.length > 0 && (
            <div className="space-y-1">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Sources ({lesson.sources.length})
              </p>
              <div className="space-y-0.5">
                {lesson.sources.slice(0, 8).map((s) => (
                  <p key={s} className="text-xs text-muted-foreground flex items-center gap-1.5">
                    <FileText className="h-3 w-3 shrink-0" />
                    {s}
                  </p>
                ))}
                {lesson.sources.length > 8 && (
                  <p className="text-xs text-muted-foreground/60">
                    +{lesson.sources.length - 8} more
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Research topics (needs_research) */}
          {lesson.researchTopics && lesson.researchTopics.length > 0 && (
            <div className="space-y-1">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Research Needed
              </p>
              <div className="flex flex-wrap gap-1">
                {lesson.researchTopics.map((rt) => (
                  <Badge
                    key={rt}
                    variant="outline"
                    className="text-xs text-amber-400 border-amber-500/30"
                  >
                    {rt}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Unmapped concepts (no_match) */}
          {lesson.unmapped && lesson.unmapped.length > 0 && (
            <div className="space-y-1">
              <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">
                Unmapped Concepts
              </p>
              <div className="flex flex-wrap gap-1">
                {lesson.unmapped.map((c) => (
                  <Badge
                    key={c}
                    variant="outline"
                    className="text-xs text-destructive border-destructive/30"
                  >
                    {c}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

/* ── Concept Verdict Row ────────────────────────────── */

function ConceptVerdictRow({
  concept,
  verdict,
  explanation,
}: {
  concept: string;
  verdict: "covered" | "thin" | "missing";
  explanation?: string;
}) {
  const icons = {
    covered: <CheckCircle2 className="h-3 w-3 text-green-400 shrink-0" />,
    thin: <AlertTriangle className="h-3 w-3 text-amber-400 shrink-0" />,
    missing: <XCircle className="h-3 w-3 text-red-400 shrink-0" />,
  };

  return (
    <div className="flex items-start gap-2 text-xs">
      {icons[verdict]}
      <span className="font-medium">{concept}</span>
      {explanation && (
        <span className="text-muted-foreground/60 flex-1 truncate">
          — {explanation}
        </span>
      )}
    </div>
  );
}

