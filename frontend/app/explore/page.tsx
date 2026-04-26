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
import { Send, Loader2, Wrench, Compass, Plus, History, X, Download, Trash2, BotMessageSquare, Sparkles } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { ConceptDeepDive } from "@/components/explore/ConceptDeepDive";
import { useVoiceStore } from "@/lib/useVoiceStore";

const mono: React.CSSProperties  = { fontFamily: "var(--font-dm-mono)" };
const serif: React.CSSProperties = { fontFamily: "var(--font-cormorant)" };
const body: React.CSSProperties  = { fontFamily: "var(--font-crimson)" };

export default function ExplorePage() {
  return <Suspense><ExplorePageInner /></Suspense>;
}

function ModeToggle({ value, onChange }: { value: "chat" | "deepdive"; onChange: (v: "chat" | "deepdive") => void }) {
  return (
    <div style={{ display: "flex", border: "1px solid rgba(240,233,214,0.12)", background: "var(--ink-2)" }}>
      {(["chat", "deepdive"] as const).map((m) => (
        <button key={m} onClick={() => onChange(m)} style={{
          ...mono, fontSize: "0.55rem", letterSpacing: "0.13em", textTransform: "uppercase",
          padding: "0.3rem 0.8rem", border: "none", cursor: "pointer", display: "flex", alignItems: "center", gap: "0.35rem",
          background: value === m ? "var(--ink-3)" : "none",
          color: value === m ? "var(--cream-0)" : "var(--cream-2)",
          borderBottom: value === m ? "1px solid var(--gold)" : "1px solid transparent",
          transition: "color 0.2s, background 0.2s",
        }}>
          {m === "chat" ? <BotMessageSquare style={{ width: "0.7rem", height: "0.7rem" }} /> : <Sparkles style={{ width: "0.7rem", height: "0.7rem" }} />}
          {m === "chat" ? "Chat" : "Deep Dive"}
        </button>
      ))}
    </div>
  );
}

function IconBtn({ onClick, title, children }: { onClick: () => void; title?: string; children: React.ReactNode }) {
  return (
    <button onClick={onClick} title={title} style={{
      ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase",
      background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)",
      display: "flex", alignItems: "center", gap: "0.3rem", padding: "0.25rem 0.5rem", transition: "color 0.2s",
    }}
    onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-1)"}
    onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}
    >{children}</button>
  );
}

function ExplorePageInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQ = searchParams.get("q") || "";
  const { messages, toolResults, streaming, toolCall, sessionId, sendMessage, loadSession, startNewSession } = useExploreStream();

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

  useEffect(() => {
    const recentMsgs = messages.slice(-6).map((m: Message) => `${m.role === "user" ? "Student" : "SAGE"}: ${m.content.slice(0, 200)}`).join("\n");
    setContext({ pageType: "explore", title: initialQ ? `Deep Dive: ${initialQ}` : "Explore", description: exploreMode === "deepdive" ? `Student is reading a deep dive on "${initialQ || "a concept"}".` : "Free-form AI exploration chat for any topic.", currentTopic: initialQ || undefined, recentMessages: recentMsgs || undefined, sendToTutor: (msg: string) => { const event = new CustomEvent("sage:voice-send", { detail: { message: msg } }); window.dispatchEvent(event); } });
    return () => clearContext();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messages, exploreMode, initialQ]);

  useEffect(() => { const token = getToken(); if (!token) router.push("/login"); }, [router]);
  useEffect(() => { if (pendingScroll.current && messages.length > 0 && messages[messages.length - 1].role === "user") { pendingScroll.current = false; latestUserRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }); } }, [messages]);
  useEffect(() => { if (textareaRef.current) { textareaRef.current.style.height = "auto"; textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 160) + "px"; } }, [input]);

  async function handleSend(content?: string) {
    const text = content ?? input.trim();
    if (!text || streaming) return;
    setInput(""); pendingScroll.current = true;
    await sendMessage(text, mode);
    textareaRef.current?.focus();
  }
  function handleKeyDown(e: React.KeyboardEvent) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }

  async function handleShowHistory() {
    const token = getToken(); if (!token) return;
    setShowHistory(true); setSessionsLoading(true);
    try { const s = await api.explore.getSessions(token); setSessions(s); } catch { setSessions([]); } finally { setSessionsLoading(false); }
  }
  async function handleLoadSession(sid: string) {
    const token = getToken(); if (!token) return;
    try { const history = await api.explore.getSessionHistory(sid, token); loadSession(sid, history.map((m) => ({ id: m.id, role: m.role as "user" | "assistant", content: m.content }))); setShowHistory(false); } catch {}
  }
  async function handleDeleteSession(sid: string) {
    const token = getToken(); if (!token) return;
    try { await api.explore.deleteSession(sid, token); setSessions((prev) => prev.filter((s) => s.id !== sid)); if (sessionId === sid) startNewSession(); } catch {}
  }
  function handleSaveConversation() {
    if (messages.length === 0) return;
    const date = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    const lines = ["# Exploration Session", `*Saved on ${date}*`, "", "---", ""];
    for (const msg of messages) { const label = msg.role === "user" ? "**You**" : "**Tutor**"; const content = msg.content.replace(/<quiz>[\s\S]*?<\/quiz>/g, "[Interactive Quiz]").trim(); lines.push(`### ${label}`, "", content, "", "---", ""); }
    const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
    const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = `exploration-${new Date().toISOString().slice(0, 10)}.md`; document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }

  return (
    <div className="flex flex-col h-dvh overflow-hidden" style={{ background: "var(--ink)", color: "var(--cream-0)" }}>
      <AppHeader leftSlot={
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <ModeToggle value={exploreMode} onChange={setExploreMode} />
          {exploreMode === "chat" && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.1rem" }}>
              {messages.length > 0 && <IconBtn onClick={handleSaveConversation} title="Save"><Download style={{ width: "0.7rem", height: "0.7rem" }} />Save</IconBtn>}
              <IconBtn onClick={() => { startNewSession(); setShowHistory(false); }} title="New"><Plus style={{ width: "0.7rem", height: "0.7rem" }} />New</IconBtn>
              <IconBtn onClick={handleShowHistory} title="History"><History style={{ width: "0.7rem", height: "0.7rem" }} />History</IconBtn>
            </div>
          )}
        </div>
      } />

      {/* History drawer */}
      {showHistory && (
        <div style={{ borderBottom: "1px solid rgba(240,233,214,0.08)", background: "var(--ink-1)", flexShrink: 0 }}>
          <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "1rem 1.5rem" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "0.75rem" }}>
              <span style={{ ...mono, fontSize: "0.55rem", letterSpacing: "0.14em", textTransform: "uppercase", color: "var(--cream-2)" }}>Previous Sessions</span>
              <button onClick={() => setShowHistory(false)} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", display: "flex" }}><X style={{ width: "0.8rem", height: "0.8rem" }} /></button>
            </div>
            {sessionsLoading ? (
              <p style={{ ...mono, fontSize: "0.55rem", color: "var(--cream-2)", letterSpacing: "0.1em" }}>Loading…</p>
            ) : sessions.length === 0 ? (
              <p style={{ ...body, fontSize: "0.9rem", color: "var(--cream-2)" }}>No previous sessions yet.</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.25rem", maxHeight: "12rem", overflowY: "auto" }}>
                {sessions.map((s) => (
                  <div key={s.id} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                    <button onClick={() => handleLoadSession(s.id)} style={{ flex: 1, textAlign: "left", padding: "0.5rem 0.75rem", background: "none", border: "1px solid rgba(240,233,214,0.06)", cursor: "pointer", color: "var(--cream-1)", display: "flex", alignItems: "center", justifyContent: "space-between", gap: "1rem" }}>
                      <span style={{ ...body, fontSize: "0.9rem", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.title}</span>
                      <span style={{ ...mono, fontSize: "0.5rem", letterSpacing: "0.1em", color: "var(--cream-2)", flexShrink: 0 }}>{new Date(s.updated_at).toLocaleDateString()}</span>
                    </button>
                    <button onClick={() => handleDeleteSession(s.id)} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--cream-2)", display: "flex", padding: "0.25rem", transition: "color 0.2s" }} onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--rose)"} onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = "var(--cream-2)"}><Trash2 style={{ width: "0.75rem", height: "0.75rem" }} /></button>
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
            <div className="flex-1 flex flex-col items-center justify-center px-6">
              <div style={{ width: "3rem", height: "3rem", background: "rgba(196,152,90,0.12)", border: "1px solid rgba(196,152,90,0.25)", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: "1rem" }}>
                <Compass style={{ width: "1.4rem", height: "1.4rem", color: "var(--gold)" }} />
              </div>
              <h2 style={{ ...serif, fontWeight: 700, fontStyle: "italic", fontSize: "clamp(1.6rem,4vw,2.4rem)", color: "var(--cream-0)", marginBottom: "0.4rem", lineHeight: 1.1 }}>
                Start exploring<span style={{ color: "var(--gold)" }}>.</span>
              </h2>
              <p style={{ ...body, fontSize: "1rem", color: "var(--cream-1)", marginBottom: "2rem" }}>Ask anything — a question, a problem, or just curiosity</p>

              <div style={{ width: "100%", maxWidth: "42rem", marginBottom: "1.5rem" }}>
                <div style={{ display: "flex", gap: "0.75rem", alignItems: "flex-end", background: "var(--ink-1)", border: "1px solid rgba(240,233,214,0.1)", padding: "0.75rem 1rem" }}>
                  <textarea ref={textareaRef} value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="Ask anything…" disabled={streaming} rows={1}
                    style={{ flex: 1, resize: "none", background: "none", border: "none", outline: "none", ...body, fontSize: "1rem", color: "var(--cream-0)", minHeight: "1.75rem", maxHeight: "7.5rem" }} />
                  <button onClick={() => handleSend()} disabled={!input.trim() || streaming} style={{ background: streaming || !input.trim() ? "rgba(196,152,90,0.3)" : "var(--gold)", border: "none", cursor: streaming || !input.trim() ? "not-allowed" : "pointer", color: "var(--ink)", padding: "0.5rem", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transition: "background 0.2s" }}>
                    {streaming ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> : <Send style={{ width: "1rem", height: "1rem" }} />}
                  </button>
                </div>
              </div>

              <ExploreSuggestedPrompts onSelect={(p) => handleSend(p)} />
            </div>
          ) : (
            <>
              <div className="flex-1 overflow-y-auto min-h-0 thin-scrollbar">
                <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "1.5rem" }}>
                  <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
                    {messages.map((m, i) => {
                      const isLastUser = m.role === "user" && !messages.slice(i + 1).some((msg) => msg.role === "user");
                      return (
                        <div key={m.id} ref={isLastUser ? latestUserRef : undefined}>
                          <MessageBubble role={m.role} content={m.content} isStreaming={streaming && i === messages.length - 1} onSendMessage={(msg) => handleSend(msg)} />
                        </div>
                      );
                    })}
                    {toolResults.filter((tr) => tr.toolName === "search_web").map((tr) => {
                      const data = tr.result as { query?: string; results?: { title: string; url: string; snippet: string }[] };
                      return <ResourceCard key={tr.id} resources={data.results ?? []} query={data.query} />;
                    })}
                    {toolCall && (
                      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", ...mono, fontSize: "0.55rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "var(--cream-2)", padding: "0.5rem 0.75rem", background: "var(--ink-2)", width: "fit-content" }}>
                        <Wrench style={{ width: "0.7rem", height: "0.7rem" }} className="animate-spin" />
                        {toolCall.name.replace(/_/g, " ")}…
                      </div>
                    )}
                    {streaming && !toolCall && (
                      <div style={{ display: "flex", gap: "0.3rem", paddingLeft: "0.25rem" }}>
                        {[0, 150, 300].map((delay) => (
                          <span key={delay} style={{ width: "0.45rem", height: "0.45rem", background: "var(--gold)", borderRadius: "50%" }} className="animate-bounce" style={{ animationDelay: `${delay}ms` }} />
                        ))}
                      </div>
                    )}
                    <div ref={bottomRef} style={{ minHeight: "70vh" }} />
                  </div>
                </div>
              </div>

              <div style={{ borderTop: "1px solid rgba(240,233,214,0.08)", background: "var(--ink-1)", flexShrink: 0 }}>
                <ExplainDifferentlyBar activeMode={mode} onModeChange={setMode} />
                <div style={{ maxWidth: "48rem", margin: "0 auto", padding: "0.75rem 1rem" }}>
                  <div style={{ display: "flex", gap: "0.75rem", alignItems: "flex-end" }}>
                    <textarea ref={textareaRef} value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="Ask anything…" disabled={streaming} rows={1}
                      style={{ flex: 1, resize: "none", background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.1)", outline: "none", padding: "0.65rem 0.9rem", ...body, fontSize: "1rem", color: "var(--cream-0)", minHeight: "2.75rem", maxHeight: "10rem" }} />
                    <button onClick={() => handleSend()} disabled={!input.trim() || streaming} style={{ background: streaming || !input.trim() ? "rgba(196,152,90,0.3)" : "var(--gold)", border: "none", cursor: streaming || !input.trim() ? "not-allowed" : "pointer", color: "var(--ink)", padding: "0.65rem 0.75rem", display: "flex", alignItems: "center", flexShrink: 0, transition: "background 0.2s" }}>
                      {streaming ? <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" /> : <Send style={{ width: "1rem", height: "1rem" }} />}
                    </button>
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
