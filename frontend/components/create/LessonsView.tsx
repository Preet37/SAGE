"use client";
import { useState, useEffect, useCallback } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { BookOpen, Eye, Loader2, Library } from "lucide-react";
import { api, API_URL } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { streamSSE, SSEEvent } from "@/lib/useCreatorStream";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { useCreatorState } from "@/lib/useCreatorState";

interface LessonsViewProps {
  state: ReturnType<typeof useCreatorState>;
}

interface LessonData {
  slug: string;
  title: string;
  content?: string;
  reference_kb?: string;
  summary?: string;
  concepts?: string[];
}

export function LessonsView({ state }: LessonsViewProps) {
  const { outline, draft, phase } = state;
  const [lessons, setLessons] = useState<Record<string, LessonData>>({});
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<"notes" | "kb">("notes");
  const [loadingContent, setLoadingContent] = useState(false);
  const [generatingKb, setGeneratingKb] = useState(false);
  const [kbProgress, setKbProgress] = useState("");

  // Load lesson data from draft
  const loadLessons = useCallback(async () => {
    const token = getToken();
    if (!token || !draft) return;
    setLoadingContent(true);
    try {
      const d = await api.courseCreator.getDraft(draft.id, token);
      const data = d.data as Record<string, unknown>;
      const lessonMap = (data.lessons || {}) as Record<string, LessonData>;
      setLessons(lessonMap);

      // Auto-select first lesson with content
      if (!selectedSlug) {
        const firstWithContent = Object.values(lessonMap).find(
          (l) => l.content,
        );
        if (firstWithContent) setSelectedSlug(firstWithContent.slug);
      }
    } catch (err) {
      console.error("Failed to load lessons:", err);
    } finally {
      setLoadingContent(false);
    }
  }, [draft, selectedSlug]);

  useEffect(() => {
    if (phase === "reviewing" || phase === "published" || phase === "building") {
      loadLessons();
    }
  }, [phase, loadLessons]);

  const generateReferenceKb = useCallback(() => {
    if (!draft) return;
    setGeneratingKb(true);
    setKbProgress("Starting reference KB generation...");

    streamSSE(
      `/course-creator/drafts/${draft.id}/wiki-reference-kb`,
      {},
      (event: SSEEvent) => {
        if (event.type === "progress") {
          const title = event.lesson_title as string || "";
          const status = event.status as string || "";
          setKbProgress(`${title}: ${status}`);
        } else if (event.type === "status") {
          setKbProgress(event.message as string || "Processing...");
        }
      },
      () => {
        setGeneratingKb(false);
        setKbProgress("");
        loadLessons();
      },
      (err) => {
        console.error("Reference KB generation error:", err);
        setGeneratingKb(false);
        setKbProgress("");
      },
    );
  }, [draft, loadLessons]);

  if (phase === "shaping") {
    return (
      <EmptyState>
        Generate content first to preview lessons here.
      </EmptyState>
    );
  }

  const selected = selectedSlug ? lessons[selectedSlug] : null;

  // Build ordered lesson list from outline
  const orderedLessons: { moduleTitle: string; lessons: LessonData[] }[] = [];
  if (outline) {
    for (const mod of outline.modules) {
      const modLessons: LessonData[] = [];
      for (const ol of mod.lessons) {
        const data = lessons[ol.slug];
        if (data) modLessons.push(data);
        else modLessons.push({ slug: ol.slug, title: ol.title });
      }
      orderedLessons.push({ moduleTitle: mod.title, lessons: modLessons });
    }
  }

  const markdownComponents = {
    // Use span (inline) instead of figure (block) to avoid invalid <p>→<figure> nesting.
    // ReactMarkdown wraps images in <p>, so block elements inside cause hydration errors.
    img: ({ src, alt, ...props }: React.ImgHTMLAttributes<HTMLImageElement>) => {
      let resolvedSrc = (typeof src === "string" ? src : "") || "";
      if (resolvedSrc.startsWith("/api/")) {
        resolvedSrc = `${API_URL}${resolvedSrc}`;
      }
      return (
        <span className="block my-4">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={resolvedSrc}
            alt={alt || ""}
            className="rounded-lg max-w-full h-auto border border-border"
            loading="lazy"
            {...props}
          />
          {alt && (
            <span className="block text-xs text-muted-foreground mt-1.5 text-center italic">
              {alt}
            </span>
          )}
        </span>
      );
    },
  };

  return (
    <div className="flex flex-1 min-h-0">
      {/* Sidebar */}
      <div className="w-64 border-r border-border shrink-0 flex flex-col min-h-0">
        <div className="px-4 py-3 border-b border-border shrink-0">
          <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
            Lessons
          </h3>
        </div>
        <ScrollArea className="flex-1 min-h-0">
          <div className="py-1">
            {orderedLessons.map((group, gi) => (
              <div key={group.moduleTitle} className={gi > 0 ? "mt-1" : ""}>
                {/* Module header — clearly a section label, not clickable */}
                <div className="mx-2 mb-0.5 mt-3 px-2 py-1.5 rounded-sm bg-muted/60 border-l-2 border-primary/40">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider leading-tight">
                    {group.moduleTitle}
                  </p>
                </div>
                {group.lessons.map((lesson) => (
                  <button
                    key={lesson.slug}
                    onClick={() => setSelectedSlug(lesson.slug)}
                    className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                      selectedSlug === lesson.slug
                        ? "bg-accent font-medium text-accent-foreground"
                        : "text-foreground hover:bg-accent/40"
                    } ${!lesson.content ? "opacity-40 cursor-not-allowed" : ""}`}
                    disabled={!lesson.content}
                  >
                    {lesson.title}
                  </button>
                ))}
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Content area */}
      <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
        {selected?.content ? (
          <>
            {/* Toolbar */}
            <div className="flex items-center justify-between px-6 py-3 border-b border-border shrink-0">
              <h2 className="text-sm font-medium truncate">{selected.title}</h2>
              <div className="flex items-center gap-1.5 shrink-0">
                <Button
                  variant={viewMode === "notes" ? "secondary" : "ghost"}
                  size="sm"
                  className="gap-1.5 text-xs h-7"
                  onClick={() => setViewMode("notes")}
                >
                  <Eye className="h-3 w-3" />
                  Notes
                </Button>
                {selected.reference_kb ? (
                  <Button
                    variant={viewMode === "kb" ? "secondary" : "ghost"}
                    size="sm"
                    className="gap-1.5 text-xs h-7"
                    onClick={() => setViewMode("kb")}
                  >
                    <BookOpen className="h-3 w-3" />
                    Reference KB
                  </Button>
                ) : (
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5 text-xs h-7"
                    onClick={generateReferenceKb}
                    disabled={generatingKb}
                  >
                    {generatingKb ? (
                      <Loader2 className="h-3 w-3 animate-spin" />
                    ) : (
                      <Library className="h-3 w-3" />
                    )}
                    {generatingKb ? "Generating KB..." : "Generate Reference KB"}
                  </Button>
                )}
              </div>
            </div>
            {generatingKb && kbProgress && (
              <div className="px-6 py-2 bg-muted/30 border-b border-border text-xs text-muted-foreground flex items-center gap-2 shrink-0">
                <Loader2 className="h-3 w-3 animate-spin shrink-0" />
                <span className="truncate">{kbProgress}</span>
              </div>
            )}

            {/* Content */}
            <ScrollArea className="flex-1 min-h-0">
              <div className="px-8 py-6 max-w-3xl">
                {selected.concepts && selected.concepts.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    {selected.concepts.map((c) => (
                      <Badge key={c} variant="secondary" className="text-xs">
                        {c}
                      </Badge>
                    ))}
                  </div>
                )}
                <div className="prose dark:prose-invert max-w-none prose-headings:font-semibold prose-headings:text-foreground prose-p:text-muted-foreground prose-p:leading-relaxed prose-code:bg-slate-100 prose-code:text-slate-800 prose-code:rounded prose-code:px-1 prose-code:py-0.5 prose-pre:bg-slate-100 prose-pre:text-slate-800 prose-pre:rounded-lg prose-pre:p-4 prose-strong:text-foreground prose-a:text-primary prose-li:text-muted-foreground">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={markdownComponents}
                  >
                    {viewMode === "notes"
                      ? selected.content
                      : selected.reference_kb || "*No reference KB generated*"}
                  </ReactMarkdown>
                </div>
              </div>
            </ScrollArea>
          </>
        ) : loadingContent ? (
          <div className="p-8 space-y-4">
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-5/6" />
          </div>
        ) : (
          <EmptyState>Select a lesson from the sidebar to preview.</EmptyState>
        )}
      </div>
    </div>
  );
}

function EmptyState({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-center h-full text-sm text-muted-foreground px-8 text-center">
      {children}
    </div>
  );
}
