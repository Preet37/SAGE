"use client";
import { useState, useRef, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getToken } from "@/lib/auth";
import { api, ExplorationSessionResponse } from "@/lib/api";
import { useExploreStream, Message } from "@/lib/useExploreStream";
import { MessageBubble } from "@/components/tutor/MessageBubble";
import { ResourceCard } from "@/components/tutor/ResourceCard";
import { ExplainDifferentlyBar } from "@/components/tutor/ExplainDifferentlyBar";
import { ExploreSuggestedPrompts } from "@/components/explore/ExploreSuggestedPrompts";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Send,
  Loader2,
  Wrench,
  Compass,
  Plus,
  History,
  X,
  Download,
  Trash2,
  BotMessageSquare,
  Sparkles,
} from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { ConceptDeepDive } from "@/components/explore/ConceptDeepDive";
import { cn } from "@/lib/utils";
import { useVoiceStore } from "@/lib/useVoiceStore";

export default function ExplorePage() {
  return (
    <Suspense>
      <ExplorePageInner />
    </Suspense>
  );
}

function ExplorePageInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQ = searchParams.get("q") || "";
  const {
    messages,
    toolResults,
    streaming,
    toolCall,
    sessionId,
    sendMessage,
    loadSession,
    startNewSession,
  } = useExploreStream();

  const [input, setInput] = useState("");
  const [mode, setMode] = useState("default");
  const [exploreMode, setExploreMode] = useState<"chat" | "deepdive">(initialQ ? "deepdive" : "chat");
  const [showHistory, setShowHistory] = useState(false);
  const [sessions, setSessions] = useState<ExplorationSessionResponse[]>([]);
  const [sessionsLoading, setSessionsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const latestUserRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const pendingScroll = useRef(false);

  const { setContext, clearContext } = useVoiceStore();

  // Push explore page context to voice agent
  useEffect(() => {
    const recentMsgs = messages
      .slice(-6)
      .map((m: Message) => `${m.role === "user" ? "Student" : "SAGE"}: ${m.content.slice(0, 200)}`)
      .join("\n");
    setContext({
      pageType: "explore",
      title: initialQ ? `Deep Dive: ${initialQ}` : "Explore",
      description: exploreMode === "deepdive"
        ? `Student is reading a deep dive on "${initialQ || "a concept"}".`
        : "Free-form AI exploration chat for any topic.",
      currentTopic: initialQ || undefined,
      recentMessages: recentMsgs || undefined,
      sendToTutor: (msg: string) => {
        const event = new CustomEvent("sage:voice-send", { detail: { message: msg } });
        window.dispatchEvent(event);
      },
    });
    return () => clearContext();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messages, exploreMode, initialQ]);

  useEffect(() => {
    const token = getToken();
    if (!token) router.push("/login");
  }, [router]);

  useEffect(() => {
    if (pendingScroll.current && messages.length > 0 && messages[messages.length - 1].role === "user") {
      pendingScroll.current = false;
      latestUserRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 160) + "px";
    }
  }, [input]);

  async function handleSend(content?: string) {
    const text = content ?? input.trim();
    if (!text || streaming) return;
    setInput("");
    pendingScroll.current = true;
    await sendMessage(text, mode);
    textareaRef.current?.focus();
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  async function handleShowHistory() {
    const token = getToken();
    if (!token) return;
    setShowHistory(true);
    setSessionsLoading(true);
    try {
      const s = await api.explore.getSessions(token);
      setSessions(s);
    } catch {
      setSessions([]);
    } finally {
      setSessionsLoading(false);
    }
  }

  async function handleLoadSession(sid: string) {
    const token = getToken();
    if (!token) return;
    try {
      const history = await api.explore.getSessionHistory(sid, token);
      loadSession(
        sid,
        history.map((m) => ({
          id: m.id,
          role: m.role as "user" | "assistant",
          content: m.content,
        }))
      );
      setShowHistory(false);
    } catch (err) {
      console.error("Failed to load session:", err);
    }
  }

  async function handleDeleteSession(sid: string) {
    const token = getToken();
    if (!token) return;
    try {
      await api.explore.deleteSession(sid, token);
      setSessions((prev) => prev.filter((s) => s.id !== sid));
      if (sessionId === sid) startNewSession();
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  }

  function handleNewSession() {
    startNewSession();
    setShowHistory(false);
  }

  function handleSaveConversation() {
    if (messages.length === 0) return;
    const date = new Date().toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    const lines = [
      "# Exploration Session",
      `*Saved on ${date}*`,
      "",
      "---",
      "",
    ];
    for (const msg of messages) {
      const label = msg.role === "user" ? "**You**" : "**Tutor**";
      const content = msg.content
        .replace(/<quiz>[\s\S]*?<\/quiz>/g, "[Interactive Quiz]")
        .trim();
      lines.push(`### ${label}`, "", content, "", "---", "");
    }
    const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `exploration-${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  return (
    <div className="flex flex-col h-dvh bg-background overflow-hidden">
      <AppHeader
        leftSlot={
          <>
            {/* Chat / Deep Dive toggle */}
            <div className="flex items-center rounded-lg border border-border bg-muted/50 p-0.5">
              <button
                onClick={() => setExploreMode("chat")}
                className={cn(
                  "flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all",
                  exploreMode === "chat"
                    ? "bg-background text-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                <BotMessageSquare className="h-3.5 w-3.5" />
                Chat
              </button>
              <button
                onClick={() => setExploreMode("deepdive")}
                className={cn(
                  "flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all",
                  exploreMode === "deepdive"
                    ? "bg-background text-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                <Sparkles className="h-3.5 w-3.5" />
                Deep Dive
              </button>
            </div>
            {exploreMode === "chat" && (
              <div className="flex items-center gap-1 ml-1">
                {messages.length > 0 && (
                  <Button variant="ghost" size="sm" onClick={handleSaveConversation} className="gap-1.5 text-muted-foreground hover:text-foreground">
                    <Download className="h-3.5 w-3.5" />
                    <span className="hidden sm:inline">Save</span>
                  </Button>
                )}
                <Button variant="ghost" size="sm" onClick={handleNewSession} className="gap-1.5 text-muted-foreground hover:text-foreground">
                  <Plus className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">New</span>
                </Button>
                <Button variant="ghost" size="sm" onClick={handleShowHistory} className="gap-1.5 text-muted-foreground hover:text-foreground">
                  <History className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">History</span>
                </Button>
              </div>
            )}
          </>
        }
      />

      {/* Session history drawer */}
      {showHistory && (
        <div className="border-b border-border bg-card/80 backdrop-blur">
          <div className="max-w-3xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium">Previous Sessions</h3>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={() => setShowHistory(false)}
              >
                <X className="h-3.5 w-3.5" />
              </Button>
            </div>
            {sessionsLoading ? (
              <div className="text-sm text-muted-foreground py-2">Loading...</div>
            ) : sessions.length === 0 ? (
              <div className="text-sm text-muted-foreground py-2">
                No previous sessions yet.
              </div>
            ) : (
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    className="flex items-center gap-2 group"
                  >
                    <button
                      onClick={() => handleLoadSession(s.id)}
                      className="flex-1 text-left text-sm px-3 py-2 rounded-lg hover:bg-accent transition-colors truncate"
                    >
                      <span className="font-medium">{s.title}</span>
                      <span className="text-muted-foreground ml-2 text-xs">
                        {new Date(s.updated_at).toLocaleDateString()}
                      </span>
                    </button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive"
                      onClick={() => handleDeleteSession(s.id)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {exploreMode === "deepdive" ? (
        <ConceptDeepDive initialQuery={initialQ} />
      ) : (
        <>
          {messages.length === 0 ? (
            /* Empty state — centered group like Gemini: greeting + input + chips */
            <div className="flex-1 flex flex-col items-center justify-center px-6">
              <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-3">
                <Compass className="h-6 w-6 text-primary" />
              </div>
              <h2 className="text-xl font-semibold text-foreground mb-1">Start exploring</h2>
              <p className="text-sm text-muted-foreground mb-6">Ask anything — a question, a problem, or just curiosity</p>

              <div className="w-full max-w-2xl mb-5">
                <div className="flex gap-3 items-end rounded-2xl border border-border bg-card/80 px-4 py-3 shadow-sm">
                  <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask anything..."
                    disabled={streaming}
                    rows={1}
                    className="flex-1 resize-none bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 min-h-[28px] max-h-[120px]"
                  />
                  <Button
                    onClick={() => handleSend()}
                    disabled={!input.trim() || streaming}
                    size="icon"
                    className="h-9 w-9 rounded-xl flex-shrink-0"
                  >
                    {streaming ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                  </Button>
                </div>
              </div>

              <ExploreSuggestedPrompts onSelect={(p) => handleSend(p)} />
            </div>
          ) : (
            <>
              {/* Messages — scrollable */}
              <div className="flex-1 overflow-y-auto min-h-0">
                <div className="max-w-3xl mx-auto px-6 py-6 space-y-5">
                  {messages.map((m, i) => {
                    const isLastUser = m.role === "user" && !messages.slice(i + 1).some((msg) => msg.role === "user");
                    const userQuery = m.role === "assistant"
                      ? messages.slice(0, i).reverse().find((msg) => msg.role === "user")?.content
                      : undefined;
                    return (
                      <div key={m.id} ref={isLastUser ? latestUserRef : undefined}>
                        <MessageBubble
                          role={m.role}
                          content={m.content}
                          isStreaming={streaming && i === messages.length - 1}
                          onSendMessage={(msg) => handleSend(msg)}
                          lessonTitle={initialQ || undefined}
                          userQuery={userQuery}
                        />
                      </div>
                    );
                  })}

                  {toolResults
                    .filter((tr) => tr.toolName === "search_web")
                    .map((tr) => {
                      const data = tr.result as {
                        query?: string;
                        results?: { title: string; url: string; snippet: string }[];
                      };
                      return (
                        <ResourceCard
                          key={tr.id}
                          resources={data.results ?? []}
                          query={data.query}
                        />
                      );
                    })}

                  {toolCall && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground py-2 px-4 bg-muted/50 rounded-full w-fit">
                      <Wrench className="h-3.5 w-3.5 animate-spin" />
                      <span>{toolCall.name.replace(/_/g, " ")}...</span>
                    </div>
                  )}

                  {streaming && !toolCall && (
                    <div className="flex items-center gap-1 px-1">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  )}

                  <div ref={bottomRef} className="min-h-[70vh]" />
                </div>
              </div>

              {/* Bottom bar — only when messages exist */}
              <div className="border-t border-border bg-card/50 flex-shrink-0">
                <ExplainDifferentlyBar activeMode={mode} onModeChange={setMode} />
                <div className="max-w-3xl mx-auto px-4 py-3">
                  <div className="flex gap-3 items-end">
                    <textarea
                      ref={textareaRef}
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="Ask anything — a question, a problem, or just what you're curious about..."
                      disabled={streaming}
                      rows={1}
                      className="flex-1 resize-none rounded-xl border border-border bg-background px-4 py-3 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50 min-h-[44px] max-h-[160px]"
                    />
                    <Button
                      onClick={() => handleSend()}
                      disabled={!input.trim() || streaming}
                      size="icon"
                      className="h-11 w-11 rounded-xl flex-shrink-0"
                    >
                      {streaming ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}
