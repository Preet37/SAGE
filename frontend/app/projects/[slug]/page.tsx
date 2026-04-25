"use client";
import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { getToken } from "@/lib/auth";
import { api, ProjectDetailResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MermaidBlock } from "@/components/tutor/MermaidBlock";
import { cn } from "@/lib/utils";
import {
  ArrowLeft,
  Loader2,
  ExternalLink,
  GitBranch,
  CheckCircle2,
  Rocket,
  Eye,
  BookOpen,
  Lightbulb,
  Wrench,
  Trophy,
} from "lucide-react";

function RevealSection({
  children,
  index,
}: {
  children: React.ReactNode;
  index: number;
}) {
  return (
    <>
      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(12px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
      <div
        style={{
          opacity: 0,
          animation: "fadeSlideIn 0.4s ease-out forwards",
          animationDelay: `${index * 300}ms`,
        }}
      >
        {children}
      </div>
    </>
  );
}

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
    <span
      className={cn(
        "text-xs px-2.5 py-0.5 rounded-full font-medium border",
        styles[status] || styles.coming_soon
      )}
    >
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
    <span
      className={cn(
        "text-xs px-2.5 py-0.5 rounded-full font-medium border",
        colors[difficulty] || colors.intermediate
      )}
    >
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
}

function SectionHeading({
  icon: Icon,
  title,
}: {
  icon: React.ElementType;
  title: string;
}) {
  return (
    <div className="flex items-center gap-2 mb-4">
      <Icon className="h-5 w-5 text-primary" />
      <h2 className="text-lg font-semibold text-foreground">{title}</h2>
    </div>
  );
}

export default function ProjectDetailPage() {
  const router = useRouter();
  const params = useParams();
  const slug = params.slug as string;
  const [project, setProject] = useState<ProjectDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    api.projects
      .get(slug, token)
      .then(setProject)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [slug, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center gap-4">
        <p className="text-muted-foreground">{error || "Project not found"}</p>
        <Link href="/projects">
          <Button variant="ghost" size="sm" className="gap-1.5">
            <ArrowLeft className="h-3.5 w-3.5" />
            Back to Projects
          </Button>
        </Link>
      </div>
    );
  }

  let sectionIdx = 0;

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-6 py-10">
        {/* Back button */}
        <div className="mb-6">
          <Link href="/projects">
            <Button
              variant="ghost"
              size="sm"
              className="gap-1.5 text-muted-foreground hover:text-foreground -ml-2"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Back to Projects
            </Button>
          </Link>
        </div>

        {/* Header */}
        <RevealSection index={sectionIdx++}>
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-5xl">{project.hero_emoji}</span>
              <div className="flex gap-2">
                <StatusBadge status={project.status} />
                <DifficultyBadge difficulty={project.difficulty} />
              </div>
            </div>
            <h1 className="text-3xl font-bold text-foreground mb-2">
              {project.title}
            </h1>
            <p className="text-lg text-muted-foreground mb-4">
              {project.subtitle}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {project.concepts.map((c) => (
                <Badge
                  key={c}
                  variant="secondary"
                  className="text-xs bg-primary/10 text-primary/80 border-0 px-2.5 py-0.5"
                >
                  {c}
                </Badge>
              ))}
            </div>
          </div>
        </RevealSection>

        {/* The Vision */}
        {project.vision && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={Eye} title="The Vision" />
              <div className="prose dark:prose-invert prose-sm max-w-none text-muted-foreground [&_strong]:text-foreground [&_a]:text-primary">
                <ReactMarkdown>{project.vision}</ReactMarkdown>
              </div>
            </div>
          </RevealSection>
        )}

        {/* What You'll Learn */}
        {project.learning_outcomes.length > 0 && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={Lightbulb} title="What You'll Learn" />
              <div className="space-y-3">
                {project.learning_outcomes.map((outcome, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-muted-foreground">
                      {outcome}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </RevealSection>
        )}

        {/* Architecture */}
        {project.architecture_mermaid && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={BookOpen} title="Architecture" />
              <div className="rounded-xl border border-border bg-card/50 p-6 overflow-x-auto">
                <MermaidBlock code={project.architecture_mermaid} />
              </div>
            </div>
          </RevealSection>
        )}

        {/* Try It */}
        {(project.demo_url || project.status === "demo") && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={Rocket} title="Try It" />
              {project.demo_embed && project.demo_url ? (
                <div className="rounded-xl border border-border overflow-hidden mb-4">
                  <iframe
                    src={project.demo_url}
                    className="w-full h-[500px] bg-background"
                    title={`${project.title} Demo`}
                  />
                </div>
              ) : project.demo_url ? (
                <a
                  href={project.demo_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Button className="gap-2">
                    <ExternalLink className="h-4 w-4" />
                    Open Demo
                  </Button>
                </a>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  Demo coming soon.
                </p>
              )}
            </div>
          </RevealSection>
        )}

        {/* Build It */}
        {(project.repo_url || project.setup_instructions) && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={Wrench} title="Build It" />

              {project.repo_url && (
                <a
                  href={project.repo_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 mb-4 px-4 py-2 rounded-lg border border-border bg-card hover:border-primary/50 transition-colors text-sm"
                >
                  <GitBranch className="h-4 w-4 text-primary" />
                  <span className="text-foreground font-medium">
                    {project.repo_url.replace("https://github.com/", "")}
                  </span>
                  <ExternalLink className="h-3 w-3 text-muted-foreground" />
                </a>
              )}

              {project.setup_instructions && (
                <div className="prose dark:prose-invert prose-sm max-w-none text-muted-foreground [&_strong]:text-foreground [&_code]:bg-muted [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-xs [&_pre]:bg-muted [&_pre]:rounded-lg [&_pre]:p-4">
                  <ReactMarkdown>{project.setup_instructions}</ReactMarkdown>
                </div>
              )}
            </div>
          </RevealSection>
        )}

        {/* Challenges */}
        {project.challenges.length > 0 && (
          <RevealSection index={sectionIdx++}>
            <div className="mb-10">
              <SectionHeading icon={Trophy} title="Extension Challenges" />
              <div className="space-y-3">
                {project.challenges.map((challenge, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 p-3 rounded-lg border border-border bg-card/30"
                  >
                    <span className="text-sm font-bold text-primary/60 mt-0.5 flex-shrink-0 w-6">
                      {i + 1}.
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {challenge}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </RevealSection>
        )}
      </div>
    </div>
  );
}
