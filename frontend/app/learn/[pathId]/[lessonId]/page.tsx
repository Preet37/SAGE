"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { api, LessonOut, LessonResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useVoiceActions } from "@/lib/useVoiceActions";
import { VideoPlayer } from "@/components/content/VideoPlayer";
import { TutorPanel } from "@/components/tutor/TutorPanel";
import { LessonQuiz } from "@/components/lesson/LessonQuiz";
import { NotesPanel } from "@/components/lesson/NotesPanel";
import {
  ChevronLeft,
  PanelRightOpen,
  PanelRightClose,
  GripVertical,
  BotMessageSquare,
  Trophy,
  Loader2,
  FileText,
  BookOpen,
  ExternalLink,
  PenLine,
} from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Message } from "@/lib/useTutorStream";
import { usePresence } from "@/lib/usePresence";
import Link from "next/link";
import {
  Panel,
  Group as PanelGroup,
  Separator as PanelResizeHandle,
} from "react-resizable-panels";
import { useVoiceStore } from "@/lib/useVoiceStore";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

type ActiveTab = "chat" | "quiz";
type ContentTab = "lesson" | "notes";

// Merge LessonOut + LessonResponse into one type for the page
type RichLesson = LessonOut & Partial<LessonResponse>;

function youtubeIdFromUrl(url: string | null): string | null {
  if (!url) return null;
  const m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

export default function LessonPage() {
  const router = useRouter();
  const params = useParams();
  const pathId = params.pathId as string;
  const lessonId = params.lessonId as string;

  const [lesson, setLesson] = useState<RichLesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(true);
  const [activeTab, setActiveTab] = useState<ActiveTab>("chat");
  const [contentTab, setContentTab] = useState<ContentTab>("lesson");

  usePresence({ lessonId, status: "studying" });

  const { setContext, clearContext } = useVoiceStore();
  const { register, unregister } = useVoiceActions();
  const sendToTutorRef = useCallback((msg: string) => {
    window.dispatchEvent(new CustomEvent("sage:voice-send", { detail: { message: msg } }));
  }, []);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }

    // Try learning-paths full lesson first (for user-created courses), fall back to courses
    api.learningPaths.getLesson(lessonId, token)
      .then((lr: LessonResponse) => {
        const merged: RichLesson = {
          id: lr.id,
          slug: lr.slug,
          title: lr.title,
          order: lr.order_index,
          summary: lr.summary,
          key_concepts: lr.concepts,
          estimated_minutes: 0,
          video_url: lr.youtube_id ? `https://www.youtube.com/watch?v=${lr.youtube_id}` : null,
          content: lr.content,
          youtube_id: lr.youtube_id,
          video_title: lr.video_title,
          vimeo_url: lr.vimeo_url,
          reference_kb: lr.reference_kb,
          sources_used: lr.sources_used,
          image_metadata: lr.image_metadata,
        };
        setLesson(merged);
      })
      .catch(() => {
        // Fall back to legacy courses endpoint (returns rich data now)
        api.courses.lesson(pathId, lessonId, token)
          .then((lo: LessonOut) => setLesson(lo as RichLesson))
          .catch(() => router.push(`/learn/${pathId}`));
      })
      .finally(() => setLoading(false));
  }, [pathId, lessonId, router]);

  useEffect(() => {
    if (!lesson) return;
    setContext({
      pageType: "lesson",
      title: lesson.title,
      description: lesson.summary,
      currentTopic: lesson.title,
      recentMessages: "",
      sendToTutor: sendToTutorRef,
    });
    register([
      { key: "open_quiz", description: "Switch to the quiz tab",   handler: () => setActiveTab("quiz") },
      { key: "open_chat", description: "Switch to the tutor chat", handler: () => setActiveTab("chat") },
    ]);
    return () => {
      clearContext();
      unregister(["open_quiz", "open_chat"]);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lesson]);

  if (loading) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%" }}>
        <Loader2 style={{ width: "1.25rem", height: "1.25rem", color: "var(--gold)" }} className="animate-spin" />
      </div>
    );
  }

  if (!lesson) return null;

  const ytId  = lesson.youtube_id || youtubeIdFromUrl(lesson.video_url);
  const vimUrl = lesson.vimeo_url || null;
  const hasVideo = !!(ytId || vimUrl);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", overflow: "hidden", background: "var(--ink)" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 1rem", height: "3rem", borderBottom: "1px solid rgba(240,233,214,0.07)", background: "var(--ink-1)", flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", minWidth: 0 }}>
          <Link href={`/learn/${pathId}`} style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "1.75rem", height: "1.75rem", color: "var(--cream-2)", flexShrink: 0 }}>
            <ChevronLeft style={{ width: "1rem", height: "1rem" }} />
          </Link>
          <span style={{ fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "var(--cream-0)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {lesson.title}
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexShrink: 0 }}>
          {/* Chat / Quiz tab switcher */}
          <div style={{ display: "flex", alignItems: "center", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.08)", padding: "0.15rem" }}>
            {(["chat", "quiz"] as ActiveTab[]).map((tab) => (
              <button key={tab} onClick={() => setActiveTab(tab)} style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.3rem 0.65rem", background: activeTab === tab ? "var(--ink-3)" : "transparent", color: activeTab === tab ? "var(--cream-0)" : "var(--cream-2)", border: "none", cursor: "pointer", transition: "all 0.15s" }}>
                {tab === "chat" ? <BotMessageSquare style={{ width: "0.7rem", height: "0.7rem" }} /> : <Trophy style={{ width: "0.7rem", height: "0.7rem" }} />}
                {tab}
              </button>
            ))}
          </div>

          <div style={{ width: "1px", height: "1rem", background: "rgba(240,233,214,0.1)" }} />

          {/* Notes toggle */}
          <button onClick={() => setShowContent(!showContent)} style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.48rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.35rem 0.65rem", background: "none", color: showContent ? "var(--cream-1)" : "var(--cream-2)", border: "none", cursor: "pointer" }}>
            {showContent ? <PanelRightClose style={{ width: "0.7rem", height: "0.7rem" }} /> : <PanelRightOpen style={{ width: "0.7rem", height: "0.7rem" }} />}
            <span className="hidden md:inline">Notes</span>
          </button>
        </div>
      </div>

      {/* Main area */}
      <PanelGroup orientation="horizontal" className="flex-1 overflow-hidden">
        <Panel id="primary" defaultSize={showContent ? 50 : 100} minSize={15}>
          <div style={{ height: "100%", overflow: "hidden" }}>
            {activeTab === "chat" ? (
              <TutorPanel
                lessonId={String(lesson.id)}
                lessonTitle={lesson.title}
                concepts={lesson.key_concepts}
                initialHistory={[] as Message[]}
                initialSessionId={null}
                sessions={[]}
                onSessionsChange={() => {}}
              />
            ) : (
              <LessonQuiz
                lessonId={String(lesson.id)}
                lessonTitle={lesson.title}
              />
            )}
          </div>
        </Panel>

        {showContent && (
          <>
            <PanelResizeHandle className="w-2 bg-border hover:bg-primary/30 active:bg-primary/50 transition-colors flex items-center justify-center group cursor-col-resize">
              <GripVertical className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
            </PanelResizeHandle>
            <Panel id="content" defaultSize={50} minSize={20}>
              <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "var(--ink)" }}>
                {/* Sub-tab switcher */}
                <div style={{ display: "flex", borderBottom: "1px solid rgba(240,233,214,0.07)", flexShrink: 0, background: "var(--ink-1)" }}>
                  {([["lesson", BookOpen, "Lesson"], ["notes", PenLine, "My Notes"]] as const).map(([id, Icon, label]) => (
                    <button
                      key={id}
                      onClick={() => setContentTab(id)}
                      style={{ fontFamily: "var(--font-dm-mono)", display: "flex", alignItems: "center", gap: "0.3rem", fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", padding: "0.55rem 0.9rem", background: "none", border: "none", borderBottom: contentTab === id ? "2px solid var(--gold)" : "2px solid transparent", color: contentTab === id ? "var(--cream-0)" : "var(--cream-2)", cursor: "pointer", transition: "all 0.15s" }}
                    >
                      <Icon style={{ width: "0.6rem", height: "0.6rem" }} />
                      {label}
                    </button>
                  ))}
                </div>
                {contentTab === "lesson" ? (
                  <div style={{ flex: 1, minHeight: 0, overflowY: "auto" }} className="thin-scrollbar">
                    <RichLessonPanel lesson={lesson} ytId={ytId} vimUrl={vimUrl} hasVideo={hasVideo} />
                  </div>
                ) : (
                  <div style={{ flex: 1, minHeight: 0, overflow: "auto" }}>
                    <NotesPanel lessonId={String(lesson.id)} lessonTitle={lesson.title} concepts={lesson.key_concepts} />
                  </div>
                )}
              </div>
            </Panel>
          </>
        )}
      </PanelGroup>
    </div>
  );
}

function RichLessonPanel({ lesson, ytId, vimUrl, hasVideo }: {
  lesson: RichLesson;
  ytId: string | null;
  vimUrl: string | null;
  hasVideo: boolean;
}) {
  const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
  const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
  const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

  const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  return (
    <div style={{ padding: "1.75rem 1.5rem 4rem", maxWidth: "44rem", margin: "0 auto" }}>
      {/* Title */}
      <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.5rem,3vw,2rem)", color: "var(--cream-0)", lineHeight: 1.15, marginBottom: "1rem" }}>
        {lesson.title}
      </h1>

      {/* Concept tags */}
      {lesson.key_concepts.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem", marginBottom: "1.25rem" }}>
          {lesson.key_concepts.map((c) => (
            <span key={c} style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.4rem" }}>{c}</span>
          ))}
        </div>
      )}

      {/* YouTube video */}
      {hasVideo && (
        <div style={{ marginBottom: "1.75rem" }}>
          <VideoPlayer youtubeId={ytId} vimeoUrl={vimUrl} title={lesson.video_title || lesson.title} />
          {lesson.video_title && (
            <p style={{ ...mono, fontSize: "0.48rem", letterSpacing: "0.06em", color: "var(--cream-2)", marginTop: "0.5rem" }}>
              {lesson.video_title}
            </p>
          )}
        </div>
      )}

      {/* Summary */}
      {lesson.summary && (
        <div style={{ marginBottom: "1.5rem", padding: "1rem 1.25rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)", borderLeft: "3px solid var(--gold)" }}>
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "0.5rem" }}>Summary</p>
          <p style={{ ...body, fontSize: "0.95rem", color: "var(--cream-1)", lineHeight: 1.75 }}>
            {lesson.summary}
          </p>
        </div>
      )}

      {/* Full lesson content — markdown with LaTeX */}
      {lesson.content && (
        <div style={{ marginBottom: "2rem" }}>
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "1rem", display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <BookOpen style={{ width: "0.6rem", height: "0.6rem" }} />
            Lesson Content
          </p>
          <div className="prose prose-invert prose-sm max-w-none
            prose-headings:font-semibold prose-headings:mt-6 prose-headings:mb-3
            prose-p:leading-[1.8] prose-p:my-3
            prose-li:leading-[1.75] prose-li:my-1
            prose-code:bg-white/10 prose-code:rounded prose-code:px-1.5 prose-code:py-0.5 prose-code:text-xs
            prose-pre:bg-[#0a0d12] prose-pre:rounded-xl prose-pre:p-4 prose-pre:border prose-pre:border-white/10
            prose-a:text-[var(--gold)] prose-a:no-underline hover:prose-a:underline
            prose-strong:font-semibold
            prose-blockquote:border-l-[var(--gold)]/50 prose-blockquote:pl-4 prose-blockquote:italic
            prose-table:text-sm
            prose-th:bg-white/5 prose-th:px-3 prose-th:py-2 prose-th:font-semibold
            prose-td:px-3 prose-td:py-2"
            style={{ color: "var(--cream-0)", fontFamily: "var(--font-crimson)" }}
          >
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex]}
              components={{
                img({ src, alt }) {
                  if (!src) return null;
                  const resolved = typeof src === "string" && src.startsWith("/api/") ? `${apiBase}${src}` : src;
                  return (
                    <img
                      src={resolved}
                      alt={alt || ""}
                      className="rounded-xl max-h-96 object-contain my-4 w-full"
                      loading="lazy"
                      onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
                    />
                  );
                },
              }}
            >
              {lesson.content}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {/* Reference KB / Deep background */}
      {lesson.reference_kb && (
        <details style={{ marginBottom: "1.5rem" }}>
          <summary style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", cursor: "pointer", userSelect: "none", display: "flex", alignItems: "center", gap: "0.4rem", marginBottom: "0.75rem" }}>
            <FileText style={{ width: "0.6rem", height: "0.6rem" }} />
            Deep Background & Reference
          </summary>
          <div className="prose prose-invert prose-sm max-w-none prose-p:leading-[1.75] prose-p:my-2"
            style={{ color: "var(--cream-1)", fontFamily: "var(--font-crimson)", marginTop: "0.75rem" }}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
              {lesson.reference_kb.slice(0, 4000)}
            </ReactMarkdown>
          </div>
        </details>
      )}

      {/* Sources used */}
      {lesson.sources_used && lesson.sources_used.length > 0 && (
        <div style={{ marginBottom: "1.5rem" }}>
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.75rem" }}>
            Sources & References
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
            {lesson.sources_used.map((url, i) => (
              <a
                key={i}
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                style={{ ...body, fontSize: "0.82rem", color: "var(--gold)", display: "flex", alignItems: "center", gap: "0.4rem", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
              >
                <ExternalLink style={{ width: "0.65rem", height: "0.65rem", flexShrink: 0 }} />
                {url.replace(/^https?:\/\//, "").split("/")[0]}
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Image metadata — additional diagrams from lesson research */}
      {lesson.image_metadata && lesson.image_metadata.length > 0 && (
        <div style={{ marginBottom: "1.5rem" }}>
          <p style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "0.75rem" }}>
            Diagrams & Visuals
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: "0.75rem" }}>
            {lesson.image_metadata.slice(0, 6).map((img, i) => {
              const src = img.file
                ? img.file.startsWith("http")
                  ? img.file
                  : `${apiBase}/api/wiki-images/${img.topic}/images/${img.file}`
                : img.source_url || "";
              if (!src) return null;
              return (
                <figure key={i} style={{ margin: 0 }}>
                  <img
                    src={src}
                    alt={img.alt || img.caption || "Diagram"}
                    style={{ width: "100%", height: "120px", objectFit: "contain", borderRadius: "0.5rem", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.07)" }}
                    loading="lazy"
                    onError={(e) => { (e.target as HTMLImageElement).closest("figure")!.remove(); }}
                  />
                  {img.caption && (
                    <figcaption style={{ ...mono, fontSize: "0.42rem", color: "var(--cream-2)", marginTop: "0.3rem", lineHeight: 1.4 }}>
                      {img.caption}
                    </figcaption>
                  )}
                </figure>
              );
            })}
          </div>
        </div>
      )}

      {lesson.estimated_minutes > 0 && (
        <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
          ~{lesson.estimated_minutes} min read
        </p>
      )}
    </div>
  );
}
