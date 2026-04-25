"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, LearningPathSummary } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, Share2, Sparkles, Star } from "lucide-react";
import { ShareDialog } from "@/components/ShareDialog";
import { ScrollArea } from "@/components/ui/scroll-area";

function CourseCard({
  path,
  onShare,
}: {
  path: LearningPathSummary;
  onShare?: () => void;
}) {
  return (
    <Card className="hover:border-primary/50 transition-colors group">
      <Link href={`/learn/${path.slug}`}>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10">
                {path.is_mine ? (
                  <Sparkles className="h-5 w-5 text-primary" />
                ) : (
                  <BookOpen className="h-5 w-5 text-primary" />
                )}
              </div>
              <div>
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  {path.title}
                </CardTitle>
                <div className="flex items-center gap-2 mt-1">
                  <Badge variant="secondary" className="text-xs">
                    {path.level}
                  </Badge>
                  {path.is_mine && (
                    <Badge variant="outline" className="text-xs text-purple-500 border-purple-500/30">
                      My Course
                    </Badge>
                  )}
                </div>
              </div>
            </div>
            <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
          </div>
        </CardHeader>
        <CardContent>
          <CardDescription className="line-clamp-3">{path.description}</CardDescription>
        </CardContent>
      </Link>
      {path.is_mine && onShare && (
        <div className="px-6 pb-4 pt-0">
          <Button
            variant="ghost"
            size="sm"
            className="gap-1.5 text-muted-foreground hover:text-foreground"
            onClick={(e) => { e.preventDefault(); onShare(); }}
          >
            <Share2 className="h-3.5 w-3.5" />
            Share
          </Button>
        </div>
      )}
    </Card>
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
    if (saved) {
      try { setInterests(JSON.parse(saved)); } catch { /* ignore */ }
    }
    const token = getToken();
    if (!token) { router.push("/login"); return; }
    api.learningPaths.list(token)
      .then(setPaths)
      .catch(() => router.push("/login"))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-muted-foreground">Loading learning paths...</div>
      </div>
    );
  }

  const myCourses = paths.filter(p => p.is_mine);
  const sharedWithMe = paths.filter(p => !p.is_mine && p.visibility === "private");
  const platformPaths = paths.filter(p => p.visibility === "public" && !p.is_mine);

  // Score platform paths by interest match
  const INTEREST_KEYWORDS: Record<string, string[]> = {
    "llms": ["llm", "language model", "gpt", "llama", "claude", "rlhf", "tokeniz"],
    "agents": ["agent", "reasoning", "tool use", "multi-agent", "planning"],
    "neural-networks": ["neural", "backprop", "cnn", "rnn", "transformer", "deep learning"],
    "multimodal": ["multimodal", "vision", "audio", "image"],
    "generative": ["generative", "diffusion", "gan", "vae", "nerf"],
    "ml-engineering": ["engineering", "fine-tun", "inference", "mlops", "training"],
    "rag": ["rag", "retrieval", "embedding", "vector"],
    "reinforcement": ["reinforcement", "reward", "policy", "ppo"],
    "math": ["math", "linear algebra", "calculus", "probability"],
    "safety": ["safety", "alignment", "interpretab", "red-team"],
    "nlp": ["nlp", "natural language", "tokeniz", "attention"],
    "physics-ai": ["physics", "scientific", "simulation"],
  };

  function scoreMatch(path: LearningPathSummary): number {
    if (interests.length === 0) return 0;
    const text = `${path.title} ${path.description}`.toLowerCase();
    let score = 0;
    for (const interest of interests) {
      const kws = INTEREST_KEYWORDS[interest] || [];
      for (const kw of kws) {
        if (text.includes(kw)) score++;
      }
    }
    return score;
  }

  const scoredPlatform = [...platformPaths].sort((a, b) => scoreMatch(b) - scoreMatch(a));
  const recommendedPaths = interests.length > 0 ? scoredPlatform.filter(p => scoreMatch(p) > 0) : [];
  const otherPlatform = interests.length > 0 ? scoredPlatform.filter(p => scoreMatch(p) === 0) : scoredPlatform;

  return (
    <ScrollArea className="h-full"><div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Learning Paths</h1>
        <p className="text-muted-foreground">Choose a path to start your SAGE learning journey</p>
      </div>

      {myCourses.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-purple-500" />
            My Courses
          </h2>
          <div className="grid gap-4">
            {myCourses.map((path) => (
              <CourseCard
                key={path.id}
                path={path}
                onShare={() => setShareSlug(path.slug)}
              />
            ))}
          </div>
        </div>
      )}

      {sharedWithMe.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <Share2 className="h-4 w-4 text-blue-500" />
            Shared with Me
          </h2>
          <div className="grid gap-4">
            {sharedWithMe.map((path) => (
              <CourseCard key={path.id} path={path} />
            ))}
          </div>
        </div>
      )}

      {recommendedPaths.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <Star className="h-4 w-4 text-yellow-500" />
            Recommended for You
          </h2>
          <div className="grid gap-4">
            {recommendedPaths.map((path) => (
              <CourseCard key={path.id} path={path} />
            ))}
          </div>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-primary" />
          {recommendedPaths.length > 0 ? "More Courses" : "Platform Courses"}
        </h2>
        <div className="grid gap-4">
          {otherPlatform.map((path) => (
            <CourseCard key={path.id} path={path} />
          ))}
        </div>
      </div>

      {shareSlug && (
        <ShareDialog
          slug={shareSlug}
          onClose={() => setShareSlug(null)}
        />
      )}
    </div></ScrollArea>
  );
}
