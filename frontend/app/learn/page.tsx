"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, LearningPathSummary } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { ShareDialog } from "@/components/ShareDialog";
import { ArrowRight, BookOpen, Share2, Sparkles, Star } from "lucide-react";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

const INTEREST_KEYWORDS: Record<string, string[]> = {
  "llms":            ["llm", "language model", "gpt", "llama", "claude", "rlhf", "tokeniz"],
  "agents":          ["agent", "reasoning", "tool use", "multi-agent", "planning"],
  "neural-networks": ["neural", "backprop", "cnn", "rnn", "transformer", "deep learning"],
  "multimodal":      ["multimodal", "vision", "audio", "image"],
  "generative":      ["generative", "diffusion", "gan", "vae", "nerf"],
  "ml-engineering":  ["engineering", "fine-tun", "inference", "mlops", "training"],
  "rag":             ["rag", "retrieval", "embedding", "vector"],
  "reinforcement":   ["reinforcement", "reward", "policy", "ppo"],
  "math":            ["math", "linear algebra", "calculus", "probability"],
  "safety":          ["safety", "alignment", "interpretab", "red-team"],
  "nlp":             ["nlp", "natural language", "tokeniz", "attention"],
  "physics-ai":      ["physics", "scientific", "simulation"],
};

function CourseCard({ path, onShare }: { path: LearningPathSummary; onShare?: () => void }) {
  const levelColors: Record<string, string> = {
    beginner:     "var(--sage-c)",
    intermediate: "var(--gold)",
    advanced:     "var(--rose)",
  };
  const accent = levelColors[path.level] || levelColors.beginner;

  return (
    <div
      className="topic-card"
      style={{
        background: "var(--ink-1)",
        border: "1px solid rgba(240,233,214,0.08)",
        padding: "1.25rem 1.4rem",
        position: "relative",
      }}
    >
      <Link href={`/learn/${path.slug}`} style={{ display: "block" }}>
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "1rem" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.6rem", marginBottom: "0.5rem" }}>
              <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: accent, border: `1px solid ${accent}`, padding: "0.1rem 0.4rem" }}>
                {path.level}
              </span>
              {path.is_mine && (
                <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", border: "1px solid rgba(240,233,214,0.15)", padding: "0.1rem 0.4rem" }}>
                  My Course
                </span>
              )}
            </div>
            <h3 style={{ ...serif, fontWeight: 600, fontStyle: "italic", fontSize: "1.2rem", color: "var(--cream-0)", lineHeight: 1.2, marginBottom: "0.4rem" }}>
              {path.title}
            </h3>
            <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", lineHeight: 1.55, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
              {path.description}
            </p>
          </div>
          <ArrowRight style={{ width: "1rem", height: "1rem", color: "var(--cream-2)", flexShrink: 0, marginTop: "0.15rem", transition: "color 0.2s, transform 0.2s" }} />
        </div>
      </Link>
      {path.is_mine && onShare && (
        <button
          onClick={(e) => { e.preventDefault(); onShare(); }}
          style={{
            ...mono,
            marginTop: "0.85rem",
            display: "flex",
            alignItems: "center",
            gap: "0.35rem",
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: "0.52rem",
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--cream-2)",
            padding: 0,
            transition: "color 0.2s",
          }}
          onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
          onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}
        >
          <Share2 style={{ width: "0.7rem", height: "0.7rem" }} />
          Share
        </button>
      )}
    </div>
  );
}

function SectionLabel({ icon: Icon, color, children }: { icon: React.ElementType; color: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem" }}>
      <Icon style={{ width: "0.75rem", height: "0.75rem", color, flexShrink: 0 }} />
      <span style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--cream-2)" }}>
        {children}
      </span>
      <div style={{ flex: 1, height: "1px", background: "rgba(240,233,214,0.07)" }} />
    </div>
  );
}

export default function LearnPage() {
  const router = useRouter();
  const [paths, setPaths] = useState<LearningPathSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [shareSlug, setShareSlug] = useState<string | null>(null);
  const [interests, setInterests] = useState<string[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem("sage_interests");
    if (saved) { try { setInterests(JSON.parse(saved)); } catch { /* ignore */ } }
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    api.learningPaths.list(token)
      .then(setPaths)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full" style={{ background: "var(--ink)" }}>
        <span style={{ ...mono, fontSize: "0.6rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-2)" }}>Loading…</span>
      </div>
    );
  }

  const myCourses      = paths.filter(p => p.is_mine);
  const sharedWithMe   = paths.filter(p => !p.is_mine && p.visibility === "private");
  const platformPaths  = paths.filter(p => p.visibility === "public" && !p.is_mine);

  function scoreMatch(path: LearningPathSummary) {
    if (interests.length === 0) return 0;
    const text = `${path.title} ${path.description}`.toLowerCase();
    let score = 0;
    for (const interest of interests) {
      for (const kw of (INTEREST_KEYWORDS[interest] || [])) {
        if (text.includes(kw)) score++;
      }
    }
    return score;
  }

  const scoredPlatform    = [...platformPaths].sort((a, b) => scoreMatch(b) - scoreMatch(a));
  const recommendedPaths  = interests.length > 0 ? scoredPlatform.filter(p => scoreMatch(p) > 0) : [];
  const otherPlatform     = interests.length > 0 ? scoredPlatform.filter(p => scoreMatch(p) === 0) : scoredPlatform;

  return (
    <div className="h-full overflow-y-auto thin-scrollbar" style={{ background: "var(--ink)" }}>
      <div style={{ maxWidth: "42rem", margin: "0 auto", padding: "3rem 2rem 4rem" }}>

        {/* Heading */}
        <div style={{ marginBottom: "2.5rem" }}>
          <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.6rem" }}>
            Learning Paths
          </p>
          <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.5rem, 3.5vw, 2.75rem)", lineHeight: 1.1, color: "var(--cream-0)", marginBottom: "0.5rem", whiteSpace: "nowrap" }}>
            Where would you like to go<span style={{ color: "var(--gold)" }}>?</span>
          </h1>
          <p style={{ ...body, fontSize: "1rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
            Choose a path to begin your SAGE learning journey.
          </p>
        </div>

        {/* My Courses */}
        {myCourses.length > 0 && (
          <div style={{ marginBottom: "2.5rem" }}>
            <SectionLabel icon={Sparkles} color="var(--gold)">My Courses</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {myCourses.map(p => <CourseCard key={p.id} path={p} onShare={() => setShareSlug(p.slug)} />)}
            </div>
          </div>
        )}

        {/* Shared with me */}
        {sharedWithMe.length > 0 && (
          <div style={{ marginBottom: "2.5rem" }}>
            <SectionLabel icon={BookOpen} color="var(--sage-c)">Shared with Me</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {sharedWithMe.map(p => <CourseCard key={p.id} path={p} />)}
            </div>
          </div>
        )}

        {/* Recommended */}
        {recommendedPaths.length > 0 && (
          <div style={{ marginBottom: "2.5rem" }}>
            <SectionLabel icon={Star} color="var(--gold)">Recommended for You</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {recommendedPaths.map(p => <CourseCard key={p.id} path={p} />)}
            </div>
          </div>
        )}

        {/* Platform courses */}
        <div>
          <SectionLabel icon={BookOpen} color="var(--cream-2)">{recommendedPaths.length > 0 ? "More Courses" : "Platform Courses"}</SectionLabel>
          {otherPlatform.length === 0 ? (
            <div style={{ padding: "2rem 0", textAlign: "center" }}>
              <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
                No courses available yet
              </p>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {otherPlatform.map(p => <CourseCard key={p.id} path={p} />)}
            </div>
          )}
        </div>

        {shareSlug && <ShareDialog slug={shareSlug} onClose={() => setShareSlug(null)} />}
      </div>
    </div>
  );
}
