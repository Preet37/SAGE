"use client";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { MessageBubble } from "./MessageBubble";
import { ResourceCard } from "./ResourceCard";
import { SuggestedPrompts } from "./SuggestedPrompts";
import { ExplainDifferentlyBar } from "./ExplainDifferentlyBar";
import { useTutorStream, Message } from "@/lib/useTutorStream";
import { useVoiceConversation } from "@/lib/useVoiceConversation";
import { Send, Loader2, Wrench, BotMessageSquare, Download, RotateCcw, History, Trash2, Mic, MicOff, Volume2, X } from "lucide-react";
import { api, TutorSessionResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { cn } from "@/lib/utils";

interface TutorPanelProps {
  lessonId: string;
  lessonTitle: string;
  concepts: string[];
  initialHistory?: Message[];
  initialSessionId?: string | null;
  sessions?: TutorSessionResponse[];
  onSessionsChange?: (sessions: TutorSessionResponse[]) => void;
}

export function TutorPanel({
  lessonId,
  lessonTitle,
  concepts,
  initialHistory,
  initialSessionId = null,
  sessions = [],
  onSessionsChange,
}: TutorPanelProps) {
  const { messages, toolResults, streaming, toolCall, sessionId, sendMessage, loadHistory, clearMessages } = useTutorStream(lessonId);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("default");
  const [showSessions, setShowSessions] = useState(false);
  const [showVoicePanel, setShowVoicePanel] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const latestUserRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const sessionsRef = useRef<HTMLDivElement>(null);
  const pendingScroll = useRef(false);

  const voice = useVoiceConversation({ contextOverride: lessonTitle });

  useEffect(() => {
    if (initialHistory && initialHistory.length > 0) {
      loadHistory(initialHistory, initialSessionId);
    }
  }, [lessonId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Listen for voice agent injected messages
  useEffect(() => {
    function onVoiceSend(e: Event) {
      const msg = (e as CustomEvent<{ message: string }>).detail?.message;
      if (msg) handleSend(msg);
    }
    window.addEventListener("sage:voice-send", onVoiceSend);
    return () => window.removeEventListener("sage:voice-send", onVoiceSend);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (pendingScroll.current && messages.length > 0 && messages[messages.length - 1].role === "user") {
      pendingScroll.current = false;
      latestUserRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 160) + "px";
    }
  }, [input]);

  useEffect(() => {
    if (!showSessions) return;
    function handleClickOutside(e: MouseEvent) {
      if (sessionsRef.current && !sessionsRef.current.contains(e.target as Node)) {
        setShowSessions(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [showSessions]);

  async function handleSend(content?: string) {
    const text = content ?? input.trim();
    if (!text || streaming) return;
    setInput("");
    pendingScroll.current = true;
    await sendMessage(text, mode);
    textareaRef.current?.focus();
    refreshSessions();
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  async function refreshSessions() {
    const token = getToken();
    if (!token || !onSessionsChange) return;
    try {
      const updated = await api.progress.getSessions(lessonId, token);
      onSessionsChange(updated);
    } catch { /* ignore */ }
  }

  function handleNewChat() {
    if (streaming) return;
    clearMessages();
  }

  async function handleLoadSession(sid: string) {
    const token = getToken();
    if (!token || streaming) return;
    try {
      const msgs = await api.progress.getSessionHistory(lessonId, sid, token);
      loadHistory(
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
        }),
        sid,
      );
    } catch { /* ignore */ }
    setShowSessions(false);
  }

  async function handleDeleteSession(e: React.MouseEvent, sid: string) {
    e.stopPropagation();
    const token = getToken();
    if (!token) return;
    try {
      await api.progress.deleteSession(lessonId, sid, token);
      if (onSessionsChange) {
        onSessionsChange(sessions.filter((s) => s.id !== sid));
      }
      if (sessionId === sid) {
        clearMessages();
      }
    } catch { /* ignore */ }
  }

  function handleSaveConversation() {
    if (messages.length === 0) return;

    const date = new Date().toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

    const lines = [
      `# ${lessonTitle}`,
      `*Saved on ${date}*`,
      "",
      "---",
      "",
    ];

    for (const msg of messages) {
      const label = msg.role === "user" ? "**You**" : "**Tutor**";
      const content = msg.content
        .replace(/<quiz>[\s\S]*?<\/quiz>/g, "[Interactive Quiz]")
        .replace(/<flow>[\s\S]*?<\/flow>/g, "[Interactive Diagram]")
        .replace(/<architecture>[\s\S]*?<\/architecture>/g, "[Architecture Diagram]")
        .trim();
      lines.push(`### ${label}`, "", content, "", "---", "");
    }

    const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const slug = lessonTitle.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
    a.download = `${slug}-conversation.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function formatSessionDate(iso: string) {
    return new Date(iso).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  }

  return (
    <div className="flex flex-col h-full">
      {messages.length === 0 ? (
        /* Empty state — centered group: icon + input + suggested prompts */
        <div className="flex-1 flex flex-col items-center justify-center px-6">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-3">
            <BotMessageSquare className="h-6 w-6 text-primary" />
          </div>
          <p className="text-sm text-muted-foreground mb-6">Ask a question about this lesson</p>

          <div className="w-full max-w-2xl mb-5">
            <div className="flex gap-3 items-end rounded-2xl border border-border bg-card/80 px-4 py-3 shadow-sm">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question about this lesson..."
                disabled={streaming}
                rows={1}
                className="flex-1 resize-none bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 min-h-[28px] max-h-[120px]"
              />
              {/* Voice mic button */}
              <button
                onClick={async () => {
                  if (voice.isActive) {
                    await voice.stopConversation();
                    setShowVoicePanel(false);
                  } else {
                    setShowVoicePanel(true);
                    await voice.startConversation();
                  }
                }}
                title={voice.isActive ? "End voice session" : "Start voice session"}
                className={cn(
                  "h-9 w-9 rounded-xl flex-shrink-0 flex items-center justify-center transition-all",
                  voice.isActive
                    ? "bg-violet-600 text-white ring-2 ring-violet-400/40"
                    : "hover:bg-muted text-muted-foreground hover:text-foreground"
                )}
              >
                {voice.status === "connecting" ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : voice.isActive ? (
                  <Mic className="h-4 w-4 animate-pulse" />
                ) : (
                  <Mic className="h-4 w-4" />
                )}
              </button>
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

          <SuggestedPrompts
            lessonTitle={lessonTitle}
            concepts={concepts}
            onSelect={(p) => handleSend(p)}
          />
        </div>
      ) : (
        <>
          {/* Messages — scrollable */}
          <div className="flex-1 overflow-y-auto min-h-0">
            <div className="max-w-3xl mx-auto px-6 py-6 space-y-5">
              <div className="flex justify-end gap-1 relative">
                {sessions.length > 0 && (
                  <div ref={sessionsRef} className="relative">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowSessions(!showSessions)}
                      className="gap-1.5 text-muted-foreground hover:text-foreground"
                    >
                      <History className="h-3.5 w-3.5" />
                      History ({sessions.length})
                    </Button>
                    {showSessions && (
                      <div className="absolute right-0 top-full mt-1 z-50 w-64 max-h-60 overflow-y-auto rounded-lg border border-border bg-popover shadow-lg">
                        {sessions.map((s) => (
                          <div
                            key={s.id}
                            onClick={() => handleLoadSession(s.id)}
                            className={`flex items-center justify-between px-3 py-2 text-sm cursor-pointer hover:bg-muted/50 ${
                              sessionId === s.id ? "bg-muted" : ""
                            }`}
                          >
                            <span className="truncate text-foreground">
                              {formatSessionDate(s.updated_at)}
                            </span>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-6 w-6 flex-shrink-0 text-muted-foreground hover:text-destructive"
                              onClick={(e) => handleDeleteSession(e, s.id)}
                            >
                              <Trash2 className="h-3 w-3" />
                            </Button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleNewChat}
                  disabled={streaming}
                  className="gap-1.5 text-muted-foreground hover:text-foreground"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  New Chat
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleSaveConversation}
                  className="gap-1.5 text-muted-foreground hover:text-foreground"
                >
                  <Download className="h-3.5 w-3.5" />
                  Save
                </Button>
              </div>

              {messages.map((m, i) => {
                const isLastUser = m.role === "user" && !messages.slice(i + 1).some((msg) => msg.role === "user");
                // Pass the preceding user message so sim detection reads the actual user intent
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
                      verification={m.verification}
                      lessonTitle={lessonTitle}
                      userQuery={userQuery}
                    />
                  </div>
                );
              })}

              {toolResults
                .filter((tr) => tr.toolName === "search_web")
                .map((tr) => {
                  const data = tr.result as { query?: string; results?: { title: string; url: string; snippet: string }[] };
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
            {/* Voice panel — shown when active */}
            {showVoicePanel && (
              <div className={cn(
                "mx-4 mt-3 mb-1 rounded-xl border px-4 py-3 flex items-center gap-4 transition-all",
                voice.isActive
                  ? "border-violet-400/40 bg-violet-50/50 dark:bg-violet-950/30"
                  : "border-border bg-muted/30"
              )}>
                {/* Waveform bars */}
                <div className="flex items-end gap-0.5 h-7 flex-shrink-0">
                  {Array.from({ length: 8 }).map((_, i) => (
                    <div
                      key={i}
                      className={cn(
                        "w-1 rounded-full transition-all duration-100",
                        voice.mode === "speaking" ? "bg-emerald-500" :
                        voice.mode === "listening" ? "bg-violet-500" : "bg-border"
                      )}
                      style={{
                        height: voice.mode !== "idle"
                          ? `${10 + ((i * 7 + Date.now() / 100) % 22)}px`
                          : "4px",
                      }}
                    />
                  ))}
                </div>

                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-foreground truncate">
                    {voice.status === "connecting" ? "Connecting to SAGE voice..." :
                     voice.mode === "speaking" ? "SAGE is speaking..." :
                     voice.mode === "listening" ? "Listening to you..." :
                     voice.isActive ? `Voice session active — ${lessonTitle}` :
                     "Voice session ended"}
                  </p>
                  {voice.error && (
                    <p className="text-xs text-red-500 truncate">{voice.error}</p>
                  )}
                  {voice.messages.length > 0 && (
                    <p className="text-xs text-muted-foreground truncate mt-0.5">
                      {voice.messages[voice.messages.length - 1].text}
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-1.5 flex-shrink-0">
                  {voice.isActive && (
                    <button
                      onClick={voice.toggleMute}
                      className={cn(
                        "p-1.5 rounded-lg transition-colors",
                        voice.isMuted
                          ? "bg-red-100 dark:bg-red-950 text-red-600 dark:text-red-400"
                          : "hover:bg-muted text-muted-foreground"
                      )}
                      title={voice.isMuted ? "Unmute" : "Mute"}
                    >
                      {voice.isMuted ? <MicOff className="h-3.5 w-3.5" /> : <Mic className="h-3.5 w-3.5" />}
                    </button>
                  )}
                  <button
                    onClick={async () => {
                      if (voice.isActive) {
                        await voice.stopConversation();
                        setShowVoicePanel(false);
                      } else {
                        setShowVoicePanel(false);
                      }
                    }}
                    className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground transition-colors"
                    title="Close"
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            )}

            <ExplainDifferentlyBar activeMode={mode} onModeChange={setMode} />
            <div className="max-w-3xl mx-auto px-4 py-3">
              <div className="flex gap-3 items-end">
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a question about this lesson..."
                  disabled={streaming}
                  rows={1}
                  className="flex-1 resize-none rounded-xl border border-border bg-background px-4 py-3 text-sm
                    placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring
                    disabled:opacity-50 min-h-[44px] max-h-[160px]"
                />
                {/* Voice mic button */}
                <button
                  onClick={async () => {
                    if (voice.isActive) {
                      await voice.stopConversation();
                      setShowVoicePanel(false);
                    } else {
                      setShowVoicePanel(true);
                      await voice.startConversation();
                    }
                  }}
                  title={voice.isActive ? "End voice session" : "Start voice session about this lesson"}
                  className={cn(
                    "h-11 w-11 rounded-xl flex-shrink-0 flex items-center justify-center transition-all border",
                    voice.isActive
                      ? "bg-violet-600 hover:bg-violet-700 text-white border-violet-600 ring-2 ring-violet-400/40"
                      : voice.status === "connecting"
                      ? "bg-amber-500 text-white border-amber-500 animate-pulse"
                      : "border-border hover:bg-muted text-muted-foreground hover:text-foreground"
                  )}
                >
                  {voice.status === "connecting" ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : voice.isActive && voice.mode === "speaking" ? (
                    <Volume2 className="h-4 w-4" />
                  ) : voice.isActive ? (
                    <Mic className="h-4 w-4 animate-pulse" />
                  ) : (
                    <Mic className="h-4 w-4" />
                  )}
                </button>
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
    </div>
  );
}
