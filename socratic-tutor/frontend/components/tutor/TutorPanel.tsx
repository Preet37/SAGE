"use client";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { MessageBubble } from "./MessageBubble";
import { ResourceCard } from "./ResourceCard";
import { SuggestedPrompts } from "./SuggestedPrompts";
import { ExplainDifferentlyBar } from "./ExplainDifferentlyBar";
import { useTutorStream, Message } from "@/lib/useTutorStream";
import { Send, Loader2, Wrench, BotMessageSquare, Download, RotateCcw, History, Trash2 } from "lucide-react";
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
  const bottomRef = useRef<HTMLDivElement>(null);
  const latestUserRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const sessionsRef = useRef<HTMLDivElement>(null);
  const pendingScroll = useRef(false);

  useEffect(() => {
    if (initialHistory && initialHistory.length > 0) {
      loadHistory(initialHistory, initialSessionId);
    }
  }, [lessonId]); // eslint-disable-line react-hooks/exhaustive-deps

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
        msgs.map((m) => ({
          id: m.id,
          role: m.role as "user" | "assistant",
          content: m.content,
        })),
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
                return (
                  <div key={m.id} ref={isLastUser ? latestUserRef : undefined}>
                    <MessageBubble
                      role={m.role}
                      content={m.content}
                      isStreaming={streaming && i === messages.length - 1}
                      onSendMessage={(msg) => handleSend(msg)}
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
