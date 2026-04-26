"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { api, LessonResponse, TutorSessionResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useVoiceActions } from "@/lib/useVoiceActions";
import { VideoPlayer } from "@/components/content/VideoPlayer";
import { LessonContent } from "@/components/content/LessonContent";
import { ReferenceSources } from "@/components/content/ReferenceSources";
import { TutorPanel } from "@/components/tutor/TutorPanel";
import { LessonQuiz } from "@/components/lesson/LessonQuiz";
import { Button } from "@/components/ui/button";
import {
  CheckCircle2,
  ChevronLeft,
  PanelRightOpen,
  PanelRightClose,
  GripVertical,
  BotMessageSquare,
  Trophy,
  Download,
  Headphones,
} from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
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

type ActiveTab = "chat" | "quiz";

export default function LessonPage() {
  const router = useRouter();
  const params = useParams();
  const pathId = params.pathId as string;
  const lessonId = params.lessonId as string;

  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const [completed, setCompleted] = useState(false);
  const [history, setHistory] = useState<Message[]>([]);
  const [sessions, setSessions] = useState<TutorSessionResponse[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [marking, setMarking] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const [activeTab, setActiveTab] = useState<ActiveTab>("chat");

  // Arista track: announce my presence on this lesson so peers can see me.
  usePresence({ lessonId, status: "studying" });

  // Voice context: expose lesson state to the SAGE voice agent
  const { setContext, clearContext } = useVoiceStore();
  const { register, unregister } = useVoiceActions();
  const sendToTutorRef = useCallback((msg: string) => {
    // Dispatched by the voice agent via clientTools — routes message into TutorPanel
    const event = new CustomEvent("sage:voice-send", { detail: { message: msg } });
    window.dispatchEvent(event);
  }, []);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    Promise.all([
      api.learningPaths.getLesson(lessonId, token),
      api.progress.getAll(token),
      api.progress.getSessions(lessonId, token),
    ])
      .then(async ([lessonData, prog, tutorSessions]) => {
        setLesson(lessonData);
        const progMap: Record<string, boolean> = {};
        prog.forEach((r) => {
          progMap[r.lesson_id] = r.completed;
        });
        setCompleted(!!progMap[lessonId]);
        setSessions(tutorSessions);

        if (tutorSessions.length > 0) {
          const latest = tutorSessions[0];
          setActiveSessionId(latest.id);
          const msgs = await api.progress.getSessionHistory(
            lessonId,
            latest.id,
            token
          );
          setHistory(
            msgs.map((m) => {
              let verification;
              if (m.message_meta) {
                try {
                  const meta = JSON.parse(m.message_meta);
                  if (meta?.verification) verification = meta.verification;
                } catch { /* ignore */ }
              }
              return {
                id: m.id,
                role: m.role as "user" | "assistant",
                content: m.content,
                verification,
              };
            })
          );
        }
      })
      .catch(() => router.push("/learn"))
      .finally(() => setLoading(false));
  }, [lessonId, router]);

  // Push lesson context to the voice agent whenever lesson or history changes
  useEffect(() => {
    if (!lesson) return;
    const recentMsgs = history
      .slice(-6)
      .map((m) => `${m.role === "user" ? "Student" : "Tutor"}: ${m.content.slice(0, 200)}`)
      .join("\n");
    setContext({
      pageType: "lesson",
      title: lesson.title,
      description: lesson.summary || lesson.content?.slice(0, 300) || "",
      currentTopic: lesson.title,
      recentMessages: recentMsgs,
      sendToTutor: sendToTutorRef,
    });
    // Register voice agent actions for this lesson
    register([
      {
        key: "open_quiz",
        description: "Switch to the quiz tab on the current lesson",
        handler: () => setActiveTab("quiz"),
      },
      {
        key: "open_chat",
        description: "Switch to the tutor chat tab on the current lesson",
        handler: () => setActiveTab("chat"),
      },
      {
        key: "mark_complete",
        description: "Mark the current lesson as completed",
        handler: () => handleMarkComplete(),
      },
    ]);
    return () => {
      clearContext();
      unregister(["open_quiz", "open_chat", "mark_complete"]);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lesson, history]);

  async function handleMarkComplete() {
    const token = getToken();
    if (!token || marking || completed) return;
    setMarking(true);
    try {
      await api.progress.markComplete(lessonId, token);
      setCompleted(true);
    } finally {
      setMarking(false);
    }
  }

  const handleDownloadNotes = useCallback(() => {
    if (!lesson) return;
    const md = `# ${lesson.title}\n\n${lesson.content}`;
    const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${lesson.slug || lesson.title.toLowerCase().replace(/\s+/g, "-")}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }, [lesson]);

  if (loading || !lesson) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        Loading lesson...
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-card/50 flex-shrink-0">
        <div className="flex items-center gap-2 min-w-0">
          <Link href={`/learn/${pathId}`}>
            <Button variant="ghost" size="icon" className="flex-shrink-0">
              <ChevronLeft className="h-4 w-4" />
            </Button>
          </Link>
          <h1 className="text-sm font-semibold truncate">{lesson.title}</h1>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {/* Chat / Quiz tabs */}
          <div className="flex items-center rounded-lg border border-border bg-muted/50 p-0.5">
            <button
              onClick={() => setActiveTab("chat")}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all",
                activeTab === "chat"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              <BotMessageSquare className="h-3.5 w-3.5" />
              Chat
            </button>
            <button
              onClick={() => setActiveTab("quiz")}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all",
                activeTab === "quiz"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              <Trophy className="h-3.5 w-3.5" />
              Quiz
            </button>
          </div>

          <div className="h-5 w-px bg-border" />

          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowContent(!showContent)}
            className="gap-1.5 text-muted-foreground"
          >
            {showContent ? (
              <PanelRightClose className="h-4 w-4" />
            ) : (
              <PanelRightOpen className="h-4 w-4" />
            )}
            <span className="hidden md:inline">
              {showContent ? "Hide" : "Show"} Notes
            </span>
          </Button>
          <Button
            size="sm"
            variant={completed ? "secondary" : "default"}
            onClick={handleMarkComplete}
            disabled={completed || marking}
            className="gap-1.5"
          >
            <CheckCircle2 className="h-4 w-4" />
            <span className="hidden md:inline">
              {completed ? "Completed" : marking ? "Saving..." : "Mark Complete"}
            </span>
          </Button>
        </div>
      </div>

      {/* Main area */}
      <PanelGroup
        orientation="horizontal"
        className="flex-1 overflow-hidden"
      >
        <Panel
          id="primary"
          defaultSize={showContent ? 50 : 100}
          minSize={15}
        >
          <div className="h-full overflow-hidden">
            {activeTab === "chat" ? (
              <TutorPanel
                lessonId={lesson.id}
                lessonTitle={lesson.title}
                concepts={lesson.concepts}
                initialHistory={history}
                initialSessionId={activeSessionId}
                sessions={sessions}
                onSessionsChange={setSessions}
              />
            ) : (
              <LessonQuiz
                lessonId={lesson.id}
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
                <div className="p-6 space-y-6">
                  {/* Notes action bar */}
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="gap-1.5"
                      onClick={handleDownloadNotes}
                    >
                      <Download className="h-3.5 w-3.5" />
                      Download Notes
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="gap-1.5 text-muted-foreground cursor-not-allowed"
                      disabled
                    >
                      <Headphones className="h-3.5 w-3.5" />
                      Podcast
                      <Badge variant="secondary" className="text-[10px] px-1.5 py-0 ml-0.5">
                        Soon
                      </Badge>
                    </Button>
                  </div>

                  {(lesson.youtube_id || lesson.vimeo_url) && (
                    <VideoPlayer
                      youtubeId={lesson.youtube_id}
                      vimeoUrl={lesson.vimeo_url}
                      title={lesson.video_title || undefined}
                    />
                  )}
                  <LessonContent
                    title={lesson.title}
                    content={lesson.content}
                    concepts={lesson.concepts}
                  />
                  <ReferenceSources
                    referenceKb={lesson.reference_kb}
                    sourcesUsed={lesson.sources_used}
                    imageMetadata={lesson.image_metadata}
                  />
                </div>
              </ScrollArea>
            </Panel>
          </>
        )}
      </PanelGroup>
    </div>
  );
}
