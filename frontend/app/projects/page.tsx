"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getToken } from "@/lib/auth";
import { api, ProjectSummaryResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  ArrowRight,
  Loader2,
  Hammer,
  BookOpen,
} from "lucide-react";
import { AppHeader } from "@/components/AppHeader";

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    coming_soon: "bg-zinc-500/20 text-zinc-400 border-zinc-500/30",
    demo: "bg-green-500/20 text-green-400 border-green-500/30",
    full_repo: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  };
  const labels: Record<string, string> = {
    coming_soon: "Coming Soon",
    demo: "Demo Available",
    full_repo: "Full Repo",
  };
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", styles[status] || styles.coming_soon)}>
      {labels[status] || status}
    </span>
  );
}

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const colors: Record<string, string> = {
    beginner: "bg-green-500/20 text-green-400 border-green-500/30",
    intermediate: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    advanced: "bg-red-500/20 text-red-400 border-red-500/30",
  };
  return (
    <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-medium border", colors[difficulty] || colors.intermediate)}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
}

function ProjectCard({ project }: { project: ProjectSummaryResponse }) {
  return (
    <Link href={`/projects/${project.slug}`} className="block group">
      <div className="rounded-xl border border-border bg-card hover:border-primary/50 hover:bg-card/80 transition-all duration-200 p-6 h-full flex flex-col">
        <div className="flex items-start justify-between mb-4">
          <span className="text-4xl">{project.hero_emoji}</span>
          <div className="flex gap-2">
            <StatusBadge status={project.status} />
            <DifficultyBadge difficulty={project.difficulty} />
          </div>
        </div>

        <h3 className="text-lg font-semibold text-foreground mb-1 group-hover:text-primary transition-colors">
          {project.title}
        </h3>

        <p className="text-sm text-muted-foreground mb-4 flex-1">
          {project.subtitle}
        </p>

        {project.course_slug && (
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground/70 mb-4">
            <BookOpen className="h-3 w-3" />
            <span>Part of a course</span>
          </div>
        )}

        <div className="flex flex-wrap gap-1.5 mb-4">
          {project.concepts.slice(0, 5).map((c) => (
            <Badge
              key={c}
              variant="secondary"
              className="text-[10px] bg-primary/10 text-primary/80 border-0 px-2 py-0.5"
            >
              {c}
            </Badge>
          ))}
          {project.concepts.length > 5 && (
            <Badge
              variant="secondary"
              className="text-[10px] bg-muted text-muted-foreground border-0 px-2 py-0.5"
            >
              +{project.concepts.length - 5}
            </Badge>
          )}
        </div>

        <div className="flex items-center text-sm text-primary font-medium group-hover:gap-2 gap-1 transition-all">
          View Project
          <ArrowRight className="h-4 w-4" />
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
    if (!token) {
      router.push("/login");
      return;
    }

    api.projects
      .list(token)
      .then(setProjects)
      .catch(() => router.push("/login"))
      .finally(() => setLoading(false));
  }, [router]);

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <AppHeader
        leftSlot={
          <>
            <Hammer className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm">Projects</span>
          </>
        }
      />
      <div className="max-w-5xl mx-auto px-6 py-10 w-full">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Hammer className="h-6 w-6 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">Projects</h1>
          </div>
          <p className="text-muted-foreground">
            Hands-on capstone projects that bring together concepts from your courses.
            Build real multimodal AI applications and explore the code.
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-6 w-6 animate-spin text-primary" />
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-20 text-muted-foreground">
            <Hammer className="h-10 w-10 mx-auto mb-3 opacity-40" />
            <p>No projects available yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
