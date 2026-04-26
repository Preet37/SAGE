"use client";
import { useState, useRef, useEffect } from "react";
import { MessageBubble } from "./MessageBubble";
import { ResourceCard } from "./ResourceCard";
import { SuggestedPrompts } from "./SuggestedPrompts";
import { ExplainDifferentlyBar } from "./ExplainDifferentlyBar";
import { useTutorStream, Message } from "@/lib/useTutorStream";
import { useVoiceConversation } from "@/lib/useVoiceConversation";
import { Send, Loader2, Wrench, BotMessageSquare, Download, RotateCcw, History, Trash2, Mic, MicOff, Volume2, X } from "lucide-react";
import { api, TutorSessionResponse } from "@/lib/api";
import { getToken } from "@/lib/auth";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

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
          return { id: m.id, role: m.role as "user" | "assistant", content: m.content, verification };
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
      if (onSessionsChange) onSessionsChange(sessions.filter((s) => s.id !== sid));
      if (sessionId === sid) clearMessages();
    } catch { /* ignore */ }
  }

  function handleSaveConversation() {
    if (messages.length === 0) return;
    const date = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    const lines = [`# ${lessonTitle}`, `*Saved on ${date}*`, "", "---", ""];
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
    a.download = `${lessonTitle.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}-conversation.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function formatSessionDate(iso: string) {
    return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  }

  const sendDisabled = !input.trim() || streaming;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {messages.length === 0 ? (
        /* Empty state */
        <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "2rem 2rem" }}>
          <div style={{ width: "4rem", height: "4rem", background: "rgba(196,152,90,0.12)", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: "1rem" }}>
            <BotMessageSquare style={{ width: "2rem", height: "2rem", color: "var(--gold)" }} />
          </div>
          <p style={{ ...mono, fontSize: "0.62rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-2)", marginBottom: "2rem" }}>
            Ask a question about this lesson
          </p>

          <div style={{ width: "100%", maxWidth: "52rem", marginBottom: "1.5rem" }}>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "flex-end", border: "1px solid rgba(240,233,214,0.1)", background: "var(--ink-1)", padding: "1rem 1.25rem" }}>
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question about this lesson..."
                disabled={streaming}
                rows={1}
                style={{ flex: 1, resize: "none", background: "transparent", color: "var(--cream-0)", fontSize: "1rem", fontFamily: "var(--font-crimson)", lineHeight: 1.6, border: "none", outline: "none", minHeight: "44px", maxHeight: "160px" }}
                className="placeholder:text-[var(--cream-2)] disabled:opacity-50"
              />
              <button
                onClick={async () => {
                  if (voice.isActive) { await voice.stopConversation(); setShowVoicePanel(false); }
                  else { setShowVoicePanel(true); await voice.startConversation(); }
                }}
                title={voice.isActive ? "End voice session" : "Start voice session"}
                style={{
                  width: "2.75rem", height: "2.75rem", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
                  background: voice.isActive ? "rgb(124,58,237)" : "transparent",
                  color: voice.isActive ? "white" : "var(--cream-2)",
                  border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", transition: "all 0.15s",
                }}
              >
                {voice.status === "connecting" ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> :
                 voice.isActive ? <Mic style={{ width: "1rem", height: "1rem" }} className="animate-pulse" /> :
                 <Mic style={{ width: "1rem", height: "1rem" }} />}
              </button>
              <button
                onClick={() => handleSend()}
                disabled={sendDisabled}
                style={{
                  width: "2.75rem", height: "2.75rem", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
                  background: sendDisabled ? "var(--ink-3)" : "var(--gold)",
                  color: sendDisabled ? "var(--cream-2)" : "var(--ink)",
                  border: "1px solid rgba(240,233,214,0.08)",
                  cursor: sendDisabled ? "default" : "pointer", transition: "all 0.15s",
                }}
              >
                {streaming ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> :
                 <Send style={{ width: "1rem", height: "1rem" }} />}
              </button>
            </div>
          </div>

          <SuggestedPrompts lessonTitle={lessonTitle} concepts={concepts} onSelect={(p) => handleSend(p)} />
        </div>
      ) : (
        <>
          {/* Messages — scrollable */}
          <div style={{ flex: 1, overflowY: "auto", minHeight: 0 }} className="thin-scrollbar">
            <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "1.5rem", display: "flex", flexDirection: "column", gap: "1.25rem" }}>
              {/* Actions row */}
              <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.25rem", position: "relative" }}>
                {sessions.length > 0 && (
                  <div ref={sessionsRef} style={{ position: "relative" }}>
                    <button
                      onClick={() => setShowSessions(!showSessions)}
                      style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.35rem 0.6rem", background: "none", color: "var(--cream-2)", border: "none", cursor: "pointer" }}
                    >
                      <History style={{ width: "0.75rem", height: "0.75rem" }} />
                      History ({sessions.length})
                    </button>
                    {showSessions && (
                      <div style={{ position: "absolute", right: 0, top: "100%", marginTop: "0.25rem", zIndex: 50, width: "16rem", maxHeight: "15rem", overflowY: "auto", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.1)" }}>
                        {sessions.map((s) => (
                          <div
                            key={s.id}
                            onClick={() => handleLoadSession(s.id)}
                            style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.5rem 0.75rem", cursor: "pointer", background: sessionId === s.id ? "rgba(196,152,90,0.08)" : "none", borderLeft: sessionId === s.id ? "1px solid var(--gold)" : "1px solid transparent" }}
                          >
                            <span style={{ ...mono, fontSize: "0.58rem", color: "var(--cream-1)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                              {formatSessionDate(s.updated_at)}
                            </span>
                            <button
                              onClick={(e) => handleDeleteSession(e, s.id)}
                              style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", flexShrink: 0, padding: "0.15rem", display: "flex" }}
                            >
                              <Trash2 style={{ width: "0.75rem", height: "0.75rem" }} />
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
                <button
                  onClick={handleNewChat}
                  disabled={streaming}
                  style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.35rem 0.6rem", background: "none", color: "var(--cream-2)", border: "none", cursor: streaming ? "default" : "pointer" }}
                >
                  <RotateCcw style={{ width: "0.75rem", height: "0.75rem" }} />
                  New Chat
                </button>
                <button
                  onClick={handleSaveConversation}
                  style={{ ...mono, display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.5rem", letterSpacing: "0.1em", textTransform: "uppercase", padding: "0.35rem 0.6rem", background: "none", color: "var(--cream-2)", border: "none", cursor: "pointer" }}
                >
                  <Download style={{ width: "0.75rem", height: "0.75rem" }} />
                  Save
                </button>
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
                      verification={m.verification}
                      lessonTitle={lessonTitle}
                    />
                  </div>
                );
              })}

              {toolResults.filter((tr) => tr.toolName === "search_web").map((tr) => {
                const data = tr.result as { query?: string; results?: { title: string; url: string; snippet: string }[] };
                return <ResourceCard key={tr.id} resources={data.results ?? []} query={data.query} />;
              })}

              {toolCall && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.4rem 0.75rem", background: "var(--ink-2)", width: "fit-content" }}>
                  <Wrench style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)" }} className="animate-spin" />
                  <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.08em", color: "var(--cream-2)" }}>{toolCall.name.replace(/_/g, " ")}...</span>
                </div>
              )}

              {streaming && !toolCall && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.3rem", padding: "0.25rem" }}>
                  {[0, 150, 300].map((delay) => (
                    <span key={delay} className="animate-bounce" style={{ width: "0.5rem", height: "0.5rem", background: "var(--gold)", borderRadius: "50%", display: "inline-block", animationDelay: `${delay}ms` }} />
                  ))}
                </div>
              )}

              <div ref={bottomRef} style={{ minHeight: "70vh" }} />
            </div>
          </div>

          {/* Bottom bar */}
          <div style={{ borderTop: "1px solid rgba(240,233,214,0.07)", background: "var(--ink-1)", flexShrink: 0 }}>
            {showVoicePanel && (
              <div style={{
                margin: "0.75rem 1rem 0.25rem",
                border: voice.isActive ? "1px solid rgba(167,139,250,0.3)" : "1px solid rgba(240,233,214,0.08)",
                background: voice.isActive ? "rgba(139,92,246,0.08)" : "var(--ink-2)",
                padding: "0.75rem 1rem", display: "flex", alignItems: "center", gap: "1rem",
              }}>
                <div style={{ display: "flex", alignItems: "flex-end", gap: "2px", height: "1.75rem", flexShrink: 0 }}>
                  {Array.from({ length: 8 }).map((_, i) => (
                    <div key={i} style={{
                      width: "4px", borderRadius: "2px",
                      background: voice.mode === "speaking" ? "var(--sage-c)" :
                                  voice.mode === "listening" ? "rgb(139,92,246)" : "rgba(240,233,214,0.15)",
                      height: voice.mode !== "idle" ? `${10 + ((i * 7 + Date.now() / 100) % 22)}px` : "4px",
                      transition: "all 0.1s",
                    }} />
                  ))}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ ...body, fontSize: "0.85rem", color: "var(--cream-0)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {voice.status === "connecting" ? "Connecting to SAGE voice..." :
                     voice.mode === "speaking" ? "SAGE is speaking..." :
                     voice.mode === "listening" ? "Listening to you..." :
                     voice.isActive ? `Voice session active — ${lessonTitle}` : "Voice session ended"}
                  </p>
                  {voice.error && <p style={{ fontSize: "0.75rem", color: "var(--rose)" }}>{voice.error}</p>}
                  {voice.messages.length > 0 && (
                    <p style={{ ...mono, fontSize: "0.55rem", color: "var(--cream-2)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", marginTop: "0.15rem" }}>
                      {voice.messages[voice.messages.length - 1].text}
                    </p>
                  )}
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", flexShrink: 0 }}>
                  {voice.isActive && (
                    <button
                      onClick={voice.toggleMute}
                      style={{ padding: "0.35rem", background: voice.isMuted ? "rgba(239,68,68,0.15)" : "none", color: voice.isMuted ? "rgb(248,113,113)" : "var(--cream-2)", border: "none", cursor: "pointer", display: "flex" }}
                    >
                      {voice.isMuted ? <MicOff style={{ width: "0.875rem", height: "0.875rem" }} /> : <Mic style={{ width: "0.875rem", height: "0.875rem" }} />}
                    </button>
                  )}
                  <button
                    onClick={async () => { if (voice.isActive) { await voice.stopConversation(); } setShowVoicePanel(false); }}
                    style={{ padding: "0.35rem", background: "none", color: "var(--cream-2)", border: "none", cursor: "pointer", display: "flex" }}
                  >
                    <X style={{ width: "0.875rem", height: "0.875rem" }} />
                  </button>
                </div>
              </div>
            )}

            <ExplainDifferentlyBar activeMode={mode} onModeChange={setMode} />
            <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "0.75rem 1rem" }}>
              <div style={{ display: "flex", gap: "0.75rem", alignItems: "flex-end" }}>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a question about this lesson..."
                  disabled={streaming}
                  rows={1}
                  style={{ flex: 1, resize: "none", border: "1px solid rgba(240,233,214,0.1)", background: "var(--ink-2)", color: "var(--cream-0)", padding: "0.75rem 1rem", fontSize: "0.95rem", fontFamily: "var(--font-crimson)", lineHeight: 1.6, outline: "none", minHeight: "44px", maxHeight: "160px", transition: "border-color 0.15s" }}
                  className="placeholder:text-[var(--cream-2)] disabled:opacity-50"
                />
                <button
                  onClick={async () => {
                    if (voice.isActive) { await voice.stopConversation(); setShowVoicePanel(false); }
                    else { setShowVoicePanel(true); await voice.startConversation(); }
                  }}
                  title={voice.isActive ? "End voice session" : "Start voice session about this lesson"}
                  style={{
                    width: "2.75rem", height: "2.75rem", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
                    background: voice.isActive ? "rgb(124,58,237)" : voice.status === "connecting" ? "rgb(245,158,11)" : "var(--ink-2)",
                    color: (voice.isActive || voice.status === "connecting") ? "white" : "var(--cream-2)",
                    border: "1px solid rgba(240,233,214,0.1)", cursor: "pointer", transition: "all 0.15s",
                  }}
                >
                  {voice.status === "connecting" ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> :
                   voice.isActive && voice.mode === "speaking" ? <Volume2 style={{ width: "1rem", height: "1rem" }} /> :
                   voice.isActive ? <Mic style={{ width: "1rem", height: "1rem" }} className="animate-pulse" /> :
                   <Mic style={{ width: "1rem", height: "1rem" }} />}
                </button>
                <button
                  onClick={() => handleSend()}
                  disabled={sendDisabled}
                  style={{
                    width: "2.75rem", height: "2.75rem", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
                    background: sendDisabled ? "var(--ink-3)" : "var(--gold)",
                    color: sendDisabled ? "var(--cream-2)" : "var(--ink)",
                    border: "1px solid rgba(240,233,214,0.08)",
                    cursor: sendDisabled ? "default" : "pointer", transition: "all 0.15s",
                  }}
                >
                  {streaming ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> :
                   <Send style={{ width: "1rem", height: "1rem" }} />}
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
