"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import {
  api,
  AssessmentResponse,
  SkillDimensionResponse,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  Loader2,
  Target,
  ArrowRight,
  CheckCircle2,
  RotateCcw,
  Sparkles,
  ClipboardCheck,
  Layers,
} from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

const QUICK_PROMPTS = [
  "I'm a software engineer who has used ChatGPT and built a few basic LLM apps",
  "I've built RAG applications and experimented with LangChain agents",
  "I'm completely new to AI and want to learn about agentic systems from scratch",
  "I have a strong ML background and want to learn about production agent architectures",
];

const LEVEL_CONFIG: Record<string, { label: string; color: string; barColor: string }> = {
  beginner: {
    label: "Beginner",
    color: "bg-orange-500/20 text-orange-400 border-orange-500/30",
    barColor: "bg-orange-500",
  },
  intermediate: {
    label: "Intermediate",
    color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    barColor: "bg-yellow-500",
  },
  advanced: {
    label: "Advanced",
    color: "bg-green-500/20 text-green-400 border-green-500/30",
    barColor: "bg-green-500",
  },
  expert: {
    label: "Expert",
    color: "bg-purple-500/20 text-purple-400 border-purple-500/30",
    barColor: "bg-purple-500",
  },
};

function LevelBadge({ level }: { level: string }) {
  const config = LEVEL_CONFIG[level] ?? LEVEL_CONFIG.beginner;
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", config.color)}>
      {config.label}
    </span>
  );
}

function SkillBar({ dim }: { dim: SkillDimensionResponse }) {
  const config = LEVEL_CONFIG[dim.level] ?? LEVEL_CONFIG.beginner;
  const pct = Math.round((dim.score / dim.max_score) * 100);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-sm text-foreground">{dim.name}</span>
          <LevelBadge level={dim.level} />
        </div>
        <span className="text-sm text-muted-foreground font-medium">
          {dim.score}/{dim.max_score}
        </span>
      </div>
      <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
        <div
          className={cn("h-full rounded-full transition-all duration-700", config.barColor)}
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs text-muted-foreground">{dim.description}</p>
    </div>
  );
}

export default function AssessPage() {
  const router = useRouter();
  const [backgroundText, setBackgroundText] = useState("");
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingLatest, setLoadingLatest] = useState(true);
  const [hasExisting, setHasExisting] = useState(false);
  const [view, setView] = useState<"input" | "result">("input");

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    async function loadLatest() {
      try {
        const latest = await api.assessment.getLatest(token!);
        setAssessment(latest);
        setHasExisting(true);
        setView("result");
      } catch {
        // No previous assessment — stay on input
      } finally {
        setLoadingLatest(false);
      }
    }
    loadLatest();
  }, [router]);

  async function handleAssess() {
    if (!backgroundText.trim() || loading) return;
    const token = getToken();
    if (!token) return;

    setLoading(true);
    try {
      const result = await api.assessment.assess(backgroundText.trim(), token);
      setAssessment(result);
      setHasExisting(true);
      setView("result");
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Assessment failed";
      alert(msg);
    } finally {
      setLoading(false);
    }
  }

  function handleReassess() {
    setView("input");
    setBackgroundText("");
  }

  if (loadingLatest) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <AppHeader
        leftSlot={
          <>
            <ClipboardCheck className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm">Assess</span>
          </>
        }
      />

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {view === "input" ? (
          /* ─── Input Form ─── */
          <div className="max-w-2xl mx-auto px-4 py-12">
            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Target className="h-6 w-6 text-primary" />
                  <h1 className="text-2xl font-bold text-foreground">Skill Assessment</h1>
                </div>
                <p className="text-muted-foreground">
                  Describe your background, experience, and familiarity with AI and agentic systems.
                  The more detail you provide, the more accurate the assessment.
                </p>
              </div>

              <textarea
                value={backgroundText}
                onChange={(e) => setBackgroundText(e.target.value)}
                placeholder="I'm a software engineer who has used ChatGPT and built a few basic LLM apps"
                rows={5}
                className="w-full rounded-lg border border-border bg-card px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 resize-y"
              />

              <div className="space-y-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Quick Prompts</p>
                <div className="flex flex-wrap gap-2">
                  {QUICK_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => setBackgroundText(prompt)}
                      className={cn(
                        "text-xs px-3 py-1.5 rounded-full border transition-colors text-left",
                        backgroundText === prompt
                          ? "border-primary bg-primary/10 text-primary"
                          : "border-border bg-card text-muted-foreground hover:border-primary/50 hover:text-foreground"
                      )}
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>

              <Button
                onClick={handleAssess}
                disabled={!backgroundText.trim() || loading}
                className="w-full gap-2"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Assessing your skills...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Assess My Skills
                  </>
                )}
              </Button>

              {hasExisting && (
                <button
                  onClick={() => setView("result")}
                  className="w-full text-center text-sm text-primary hover:underline"
                >
                  View latest assessment
                </button>
              )}
            </div>
          </div>
        ) : assessment ? (
          /* ─── Results View ─── */
          <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
            {/* Overall Level */}
            <div className="rounded-xl border border-border bg-card p-6 space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Overall Level</p>
                <Target className="h-5 w-5 text-muted-foreground" />
              </div>
              <LevelBadge level={assessment.overall_level} />
              <p className="text-sm text-muted-foreground leading-relaxed">{assessment.overall_summary}</p>
            </div>

            {/* Skill Dimensions */}
            <div className="rounded-xl border border-border bg-card p-6 space-y-5">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                <Target className="h-4 w-4" />
                Skill Dimensions
              </p>
              <div className="space-y-5">
                {assessment.skill_dimensions.map((dim) => (
                  <SkillBar key={dim.name} dim={dim} />
                ))}
              </div>
            </div>

            {/* Strengths & Gaps side-by-side */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Strengths */}
              <div className="rounded-xl border border-border bg-card p-6 space-y-3">
                <p className="text-xs font-medium text-green-400 uppercase tracking-wider flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4" />
                  Strengths
                </p>
                <ul className="space-y-2">
                  {assessment.strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Gaps */}
              <div className="rounded-xl border border-border bg-card p-6 space-y-3">
                <p className="text-xs font-medium text-orange-400 uppercase tracking-wider flex items-center gap-2">
                  <ArrowRight className="h-4 w-4" />
                  Identified Gaps
                </p>
                <ul className="space-y-2">
                  {assessment.gaps.map((g, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <ArrowRight className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      {g}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Recommended Starting Point */}
            <div className="rounded-xl border border-primary/30 bg-primary/5 p-6 space-y-3">
              <p className="text-xs font-medium text-primary uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="h-4 w-4" />
                Recommended Starting Point
              </p>
              <p className="text-sm text-foreground leading-relaxed">{assessment.recommendation_text}</p>
              {assessment.recommended_module_id && (
                <Button
                  onClick={() => router.push("/learn")}
                  className="gap-2 mt-2"
                  size="sm"
                >
                  Start Learning
                  <ArrowRight className="h-4 w-4" />
                </Button>
              )}
            </div>

            {/* Re-assess button */}
            <div className="flex justify-center pt-2">
              <Button variant="outline" onClick={handleReassess} className="gap-2">
                <RotateCcw className="h-4 w-4" />
                Re-assess My Skills
              </Button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
