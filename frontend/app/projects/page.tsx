"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getToken } from "@/lib/auth";
import { api, ProjectSummaryResponse } from "@/lib/api";
import { ArrowRight, Loader2, Hammer, BookOpen } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

const STATUS_LABELS: Record<string, string> = { coming_soon: "Coming Soon", demo: "Demo Available", full_repo: "Full Repo" };
const STATUS_COLORS: Record<string, string> = { coming_soon: "var(--cream-2)", demo: "var(--sage-c)", full_repo: "#60a5fa" };
const DIFF_COLORS: Record<string, string> = { beginner: "var(--sage-c)", intermediate: "var(--gold)", advanced: "var(--rose)" };

function ProjectCard({ project }: { project: ProjectSummaryResponse }) {
  const statusColor = STATUS_COLORS[project.status] || STATUS_COLORS.coming_soon;
  const diffColor = DIFF_COLORS[project.difficulty] || DIFF_COLORS.intermediate;

  return (
    <Link href={`/projects/${project.slug}`} style={{ display: "block", textDecoration: "none" }}>
      <div className="topic-card" style={{ background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.08)", padding: "1.5rem", height: "100%", display: "flex", flexDirection: "column", position: "relative" }}>
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "1rem" }}>
          <span style={{ fontSize: "2.5rem", lineHeight: 1 }}>{project.hero_emoji}</span>
          <div style={{ display: "flex", gap: "0.4rem" }}>
            <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: statusColor, border: `1px solid ${statusColor}`, padding: "0.1rem 0.4rem" }}>{STATUS_LABELS[project.status] || project.status}</span>
            <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", color: diffColor, border: `1px solid ${diffColor}`, padding: "0.1rem 0.4rem" }}>{project.difficulty}</span>
          </div>
        </div>

        <h3 style={{ ...serif, fontWeight: 600, fontStyle: "italic", fontSize: "1.25rem", color: "var(--cream-0)", lineHeight: 1.2, marginBottom: "0.4rem" }}>{project.title}</h3>
        <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)", lineHeight: 1.55, flex: 1, marginBottom: "0.75rem" }}>{project.subtitle}</p>

        {project.course_slug && (
          <div style={{ display: "flex", alignItems: "center", gap: "0.35rem", marginBottom: "0.75rem" }}>
            <BookOpen style={{ width: "0.65rem", height: "0.65rem", color: "var(--cream-2)" }} />
            <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--cream-2)" }}>Part of a course</span>
          </div>
        )}

        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem", marginBottom: "1rem" }}>
          {project.concepts.slice(0, 5).map((c) => (
            <span key={c} style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.4rem" }}>{c}</span>
          ))}
          {project.concepts.length > 5 && (
            <span style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.08em", color: "var(--cream-2)", border: "1px solid rgba(240,233,214,0.1)", padding: "0.1rem 0.4rem" }}>+{project.concepts.length - 5}</span>
          )}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "0.35rem", ...mono, fontSize: "0.52rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)" }}>
          View Project <ArrowRight style={{ width: "0.75rem", height: "0.75rem" }} />
        </div>
      </div>
    </Link>
  );
}

export default function ProjectsPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<ProjectSummaryResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    // Silently show empty state if API unavailable
    api.projects.list(token).then(setProjects).catch(() => {}).finally(() => setLoading(false));
  }, [router]);

  return (
    <div className="flex flex-col min-h-screen" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader leftSlot={
        <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <Hammer style={{ width: "0.85rem", height: "0.85rem", color: "var(--gold)" }} />
          <span style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.55rem", letterSpacing: "0.13em", textTransform: "uppercase", color: "var(--cream-1)" }}>Projects</span>
        </div>
      } />

      <div style={{ maxWidth: "56rem", margin: "0 auto", padding: "2.5rem 1.5rem 4rem", width: "100%" }}>
        <div style={{ marginBottom: "2.5rem" }}>
          <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.16em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.5rem" }}>Projects</p>
          <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(2rem,5vw,3rem)", color: "var(--cream-0)", lineHeight: 1.1, marginBottom: "0.5rem" }}>
            Build something real<span style={{ color: "var(--gold)" }}>.</span>
          </h1>
          <p style={{ ...body, fontSize: "1rem", color: "var(--cream-1)", lineHeight: 1.6 }}>
            Hands-on capstone projects that bring together concepts from your courses.
          </p>
        </div>

        {loading ? (
          <div style={{ display: "flex", justifyContent: "center", padding: "5rem 0" }}>
            <Loader2 style={{ width: "1.5rem", height: "1.5rem", color: "var(--gold)" }} className="animate-spin" />
          </div>
        ) : projects.length === 0 ? (
          <div style={{ textAlign: "center", padding: "5rem 0" }}>
            <Hammer style={{ width: "2.5rem", height: "2.5rem", color: "var(--cream-2)", margin: "0 auto 0.75rem", opacity: 0.4 }} />
            <p style={{ ...mono, fontSize: "0.58rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-2)" }}>No projects available yet</p>
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(22rem, 1fr))", gap: "0.75rem" }}>
            {projects.map((project) => <ProjectCard key={project.id} project={project} />)}
          </div>
        )}
      </div>
    </div>
  );
}
