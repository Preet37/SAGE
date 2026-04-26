"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles, RefreshCw, Check, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { useCreatorState, PendingAction } from "@/lib/useCreatorState";

const mono: React.CSSProperties = { fontFamily: "var(--font-dm-mono)" };
const body: React.CSSProperties = { fontFamily: "var(--font-crimson)" };

function stripActionBlocks(text: string): string {
  return text
    .replace(/```json\s*\n[\s\S]*?"draft_actions"[\s\S]*?\n```/g, "")
    .replace(/```json\s*\n[\s\S]*?"outline_actions"[\s\S]*?\n```/g, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

interface ChatPanelProps {
  state: ReturnType<typeof useCreatorState>;
}

export function ChatPanel({ state }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [state.chatMessages]);

  function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || state.chatStreaming) return;
    setInput("");
    state.sendChat(trimmed);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  const hasMessages = state.chatMessages.length > 0;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", minHeight: 0, background: "var(--ink-1)" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", padding: "0.65rem 1rem", borderBottom: "1px solid rgba(240,233,214,0.08)", flexShrink: 0 }}>
        <Sparkles style={{ width: "0.8rem", height: "0.8rem", color: "var(--gold)" }} />
        <span style={{ ...mono, fontSize: "0.52rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "var(--cream-1)" }}>Course Assistant</span>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", padding: "1rem" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.875rem" }}>
          {!hasMessages && <WelcomeMessage phase={state.phase} generating={state.generating} />}
          {state.chatMessages.map((msg) => (
            <div key={msg.id} style={{ display: "flex", flexDirection: "column", alignItems: msg.role === "user" ? "flex-end" : "flex-start" }}>
              <div style={{
                maxWidth: "85%",
                padding: "0.5rem 0.75rem",
                ...body, fontSize: "0.9rem", lineHeight: 1.6,
                ...(msg.role === "user"
                  ? { background: "rgba(196,152,90,0.18)", color: "var(--cream-0)", border: "1px solid rgba(196,152,90,0.25)", borderRadius: "12px 12px 2px 12px" }
                  : { background: "var(--ink-2)", color: "var(--cream-0)", border: "1px solid rgba(240,233,214,0.07)", borderRadius: "2px 12px 12px 12px" }),
              }}>
                {msg.role === "assistant" ? (
                  <div className="prose prose-sm max-w-none" style={{ color: "var(--cream-0)" }}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {stripActionBlocks(msg.content || "...")}
                    </ReactMarkdown>
                  </div>
                ) : msg.content}
              </div>
              {msg.pendingActions && msg.pendingActions.length > 0 && (
                <div style={{ marginTop: "0.5rem", maxWidth: "85%", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  {msg.pendingActions.map((action) => (
                    <PendingActionCard
                      key={action.id}
                      action={action}
                      onApprove={() => state.approvePendingAction(msg.id, action.id)}
                      onDismiss={() => state.dismissPendingAction(msg.id, action.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          ))}
          {state.chatStreaming && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", ...mono, fontSize: "0.48rem", color: "var(--cream-2)", letterSpacing: "0.08em" }}>
              <Loader2 style={{ width: "0.7rem", height: "0.7rem" }} className="animate-spin" />
              Thinking…
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div style={{ padding: "0.75rem", borderTop: "1px solid rgba(240,233,214,0.08)", flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "flex-end", gap: "0.5rem" }}>
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Refine your course..."
            rows={1}
            disabled={state.chatStreaming}
            style={{
              flex: 1, resize: "none", background: "var(--ink-2)",
              border: "1px solid rgba(240,233,214,0.1)", padding: "0.5rem 0.75rem",
              ...body, fontSize: "0.9rem", color: "var(--cream-0)", outline: "none",
              minHeight: "36px", maxHeight: "120px", lineHeight: 1.5,
              borderRadius: 0,
            }}
            onFocus={e => (e.currentTarget.style.borderColor = "rgba(196,152,90,0.4)")}
            onBlur={e => (e.currentTarget.style.borderColor = "rgba(240,233,214,0.1)")}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || state.chatStreaming}
            style={{
              width: "2.25rem", height: "2.25rem", display: "flex", alignItems: "center", justifyContent: "center",
              background: (!input.trim() || state.chatStreaming) ? "var(--ink-3)" : "var(--gold)",
              color: (!input.trim() || state.chatStreaming) ? "var(--cream-2)" : "var(--ink)",
              border: "none", cursor: (!input.trim() || state.chatStreaming) ? "not-allowed" : "pointer",
              flexShrink: 0, transition: "background 0.15s",
            }}
          >
            <Send style={{ width: "0.85rem", height: "0.85rem" }} />
          </button>
        </div>
      </div>
    </div>
  );
}

function PendingActionCard({ action, onApprove, onDismiss }: { action: PendingAction; onApprove: () => void; onDismiss: () => void }) {
  const isDone = action.status === "approved" || action.status === "skipped";
  return (
    <div style={{ background: "var(--ink-2)", border: "1px solid rgba(240,233,214,0.1)", padding: "0.6rem 0.75rem", opacity: isDone ? 0.5 : 1, transition: "opacity 0.2s" }}>
      <div style={{ display: "flex", alignItems: "flex-start", gap: "0.5rem" }}>
        <RefreshCw style={{ width: "0.75rem", height: "0.75rem", marginTop: "2px", flexShrink: 0, color: "var(--cream-2)" }} className={action.status === "loading" ? "animate-spin" : ""} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <p style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.48rem", letterSpacing: "0.08em", color: "var(--cream-0)", lineHeight: 1.4 }}>{action.label}</p>
          <p style={{ fontFamily: "var(--font-crimson)", fontSize: "0.8rem", color: "var(--cream-2)", marginTop: "2px" }}>Full lesson regeneration from wiki</p>
        </div>
      </div>
      {!isDone && action.status !== "loading" && (
        <div style={{ display: "flex", gap: "0.4rem", marginTop: "0.5rem", justifyContent: "flex-end" }}>
          <button onClick={onDismiss} style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.45rem", letterSpacing: "0.08em", color: "var(--cream-2)", background: "transparent", border: "1px solid rgba(240,233,214,0.12)", padding: "0.2rem 0.5rem", cursor: "pointer", display: "flex", alignItems: "center", gap: "0.25rem" }}>
            <X style={{ width: "0.6rem", height: "0.6rem" }} /> Skip
          </button>
          <button onClick={onApprove} style={{ fontFamily: "var(--font-dm-mono)", fontSize: "0.45rem", letterSpacing: "0.08em", color: "var(--ink)", background: "var(--gold)", border: "none", padding: "0.2rem 0.5rem", cursor: "pointer", display: "flex", alignItems: "center", gap: "0.25rem" }}>
            <Check style={{ width: "0.6rem", height: "0.6rem" }} /> Approve
          </button>
        </div>
      )}
      {action.status === "approved" && <p style={{ fontFamily: "var(--font-crimson)", fontSize: "0.8rem", color: "rgba(146,188,158,0.8)", marginTop: "0.4rem", display: "flex", alignItems: "center", gap: "0.25rem" }}><Check style={{ width: "0.65rem", height: "0.65rem" }} /> Regeneration started</p>}
      {action.status === "skipped" && <p style={{ fontFamily: "var(--font-crimson)", fontSize: "0.8rem", color: "var(--cream-2)", marginTop: "0.4rem" }}>Skipped</p>}
    </div>
  );
}

function WelcomeMessage({ phase, generating }: { phase: string; generating: boolean }) {
  if (generating) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "0.75rem", padding: "3rem 0", fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "var(--cream-2)" }}>
        <Loader2 style={{ width: "1rem", height: "1rem" }} className="animate-spin" />
        Generating your course outline…
      </div>
    );
  }

  const tips: Record<string, string[]> = {
    shaping: [
      '"Add a hands-on section on fine-tuning"',
      '"Make this more beginner-friendly"',
      '"Remove the math-heavy parts"',
      '"Split the attention lesson into two"',
    ],
    building: ["Content is being generated — feel free to ask questions!"],
    reviewing: [
      '"Remove the duplicate links in the intro lesson"',
      '"Add an example of backprop to lesson 3"',
      '"Regenerate lesson 2 with more depth on gradients"',
    ],
    published: ["Your course is published! Head to the Learn section to start studying."],
  };

  const suggestions = tips[phase] || tips.shaping;

  return (
    <div style={{ padding: "2.5rem 0.5rem", textAlign: "center" }}>
      <p style={{ fontFamily: "var(--font-crimson)", fontSize: "0.95rem", color: "var(--cream-2)", marginBottom: "1rem", lineHeight: 1.6 }}>
        {phase === "shaping" ? "Your outline is ready. Tell me how to refine it, or explore the tabs →" : phase === "reviewing" ? "Review your lessons. Tell me if anything needs changes." : ""}
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
        {suggestions.map((tip, i) => (
          <p key={i} style={{ fontFamily: "var(--font-crimson)", fontSize: "0.85rem", color: "var(--cream-2)", fontStyle: "italic", opacity: 0.7 }}>{tip}</p>
        ))}
      </div>
    </div>
  );
}
