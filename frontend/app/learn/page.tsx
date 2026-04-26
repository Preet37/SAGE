"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, CourseOut, LearningPathSummary } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { ArrowRight, BookOpen, Sparkles, Star } from "lucide-react";

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

function CourseCard({ path }: { path: CourseOut }) {
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
    </div>
  );
}

function SectionLabel({ icon: Icon, color, children }: { icon: React.ComponentType<React.SVGProps<SVGSVGElement>>; color: string; children: React.ReactNode }) {
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
  const [paths, setPaths] = useState<CourseOut[]>([]);
  const [myPaths, setMyPaths] = useState<LearningPathSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [interests, setInterests] = useState<string[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem("sage_interests");
    if (saved) { try { setInterests(JSON.parse(saved)); } catch { /* ignore */ } }
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    Promise.all([
      api.courses.list(token),
      api.learningPaths.list(token),
    ]).then(([platformPaths, userPaths]) => {
      setPaths(platformPaths);
      setMyPaths(userPaths.filter(p => p.is_mine));
    }).catch(() => {}).finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full" style={{ background: "var(--ink)" }}>
        <span style={{ ...mono, fontSize: "0.6rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-2)" }}>Loading…</span>
      </div>
    );
  }

  function scoreMatch(path: CourseOut) {
    if (interests.length === 0) return 0;
    const text = `${path.title} ${path.description} ${path.tags.join(" ")}`.toLowerCase();
    let score = 0;
    for (const interest of interests) {
      for (const kw of (INTEREST_KEYWORDS[interest] || [])) {
        if (text.includes(kw)) score++;
      }
    }
    return score;
  }

  const scoredPaths      = [...paths].sort((a, b) => scoreMatch(b) - scoreMatch(a));
  const recommendedPaths = interests.length > 0 ? scoredPaths.filter(p => scoreMatch(p) > 0) : [];
  const otherPlatform    = interests.length > 0 ? scoredPaths.filter(p => scoreMatch(p) === 0) : scoredPaths;

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

        {/* Recommended */}
        {recommendedPaths.length > 0 && (
          <div style={{ marginBottom: "2.5rem" }}>
            <SectionLabel icon={Star} color="var(--gold)">Recommended for You</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {recommendedPaths.map(p => <CourseCard key={p.id} path={p} />)}

            </div>
          </div>
        )}

        {/* My published courses */}
        {myPaths.length > 0 && (
          <div style={{ marginBottom: "2.5rem" }}>
            <SectionLabel icon={Sparkles} color="var(--sage-c)">My Courses</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {myPaths.map(p => (
                <CourseCard key={p.id} path={{ id: parseInt(p.id, 10) || 0, slug: p.slug, title: p.title, description: p.description, level: p.level, tags: [], thumbnail_url: null }} />
              ))}
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

      </div>
    </div>
  );
}
