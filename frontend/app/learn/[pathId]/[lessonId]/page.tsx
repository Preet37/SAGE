"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { api, LessonOut } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useVoiceActions } from "@/lib/useVoiceActions";
import { VideoPlayer } from "@/components/content/VideoPlayer";
import { TutorPanel } from "@/components/tutor/TutorPanel";
import { LessonQuiz } from "@/components/lesson/LessonQuiz";
import {
  ChevronLeft,
  PanelRightOpen,
  PanelRightClose,
  GripVertical,
  BotMessageSquare,
  Trophy,
  Loader2,
} from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Message } from "@/lib/useTutorStream";
import { usePresence } from "@/lib/usePresence";
import Link from "next/link";
import { cn } from "@/lib/utils";
import {
  Panel,
  Group as PanelGroup,
  Separator as PanelResizeHandle,
} from "react-resizable-panels";
import { useVoiceStore } from "@/lib/useVoiceStore";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

type ActiveTab = "chat" | "quiz";

function youtubeId(url: string | null): string | null {
  if (!url) return null;
  const m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

function vimeoUrl(url: string | null): string | null {
  if (!url) return null;
  return url.includes("vimeo.com") ? url : null;
}

export default function LessonPage() {
  const router = useRouter();
  const params = useParams();
  const pathId = params.pathId as string;
  const lessonId = params.lessonId as string;

  const [lesson, setLesson] = useState<LessonOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(false);
  const [activeTab, setActiveTab] = useState<ActiveTab>("chat");

  usePresence({ lessonId, status: "studying" });

  const { setContext, clearContext } = useVoiceStore();
  const { register, unregister } = useVoiceActions();
  const sendToTutorRef = useCallback((msg: string) => {
    window.dispatchEvent(new CustomEvent("sage:voice-send", { detail: { message: msg } }));
  }, []);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.push("/login"); return; }

    api.courses.lesson(pathId, lessonId, token)
      .then(setLesson)
      .catch(() => router.push(`/learn/${pathId}`))
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
      { key: "open_quiz",    description: "Switch to the quiz tab",    handler: () => setActiveTab("quiz") },
      { key: "open_chat",    description: "Switch to the tutor chat",  handler: () => setActiveTab("chat") },
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

  const ytId   = youtubeId(lesson.video_url);
  const vimUrl = vimeoUrl(lesson.video_url);
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
            <Panel id="content" defaultSize={50} minSize={15}>
              <ScrollArea className="h-full">
                <div style={{ padding: "1.75rem 1.5rem 3rem", maxWidth: "44rem", margin: "0 auto" }}>
                  <h1 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.5rem,3vw,2rem)", color: "var(--cream-0)", lineHeight: 1.15, marginBottom: "1rem" }}>
                    {lesson.title}
                  </h1>

                  {lesson.key_concepts.length > 0 && (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem", marginBottom: "1.25rem" }}>
                      {lesson.key_concepts.map((c) => (
                        <span key={c} style={{ ...mono, fontSize: "0.45rem", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--gold)", border: "1px solid rgba(196,152,90,0.3)", padding: "0.1rem 0.4rem" }}>{c}</span>
                      ))}
                    </div>
                  )}

                  {hasVideo && (
                    <div style={{ marginBottom: "1.5rem" }}>
                      <VideoPlayer youtubeId={ytId} vimeoUrl={vimUrl} title={lesson.title} />
                    </div>
                  )}

                  {lesson.summary && (
                    <p style={{ ...body, fontSize: "1rem", color: "var(--cream-1)", lineHeight: 1.75, marginBottom: "1.5rem" }}>
                      {lesson.summary}
                    </p>
                  )}

                  {lesson.estimated_minutes > 0 && (
                    <p style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)" }}>
                      ~{lesson.estimated_minutes} min read
                    </p>
                  )}
                </div>
              </ScrollArea>
            </Panel>
          </>
        )}
      </PanelGroup>
    </div>
  );
}
