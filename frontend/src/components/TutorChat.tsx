"use client";

import {
  forwardRef,
  useCallback,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";

import AgentBadge from "@/components/AgentBadge";
import MessageBubble, { type Message } from "@/components/MessageBubble";
import {
  type AgentEvent,
  type AudioEvent,
  type DoneEvent,
  type TokenEvent,
  type VerificationEvent,
  streamTutorChat,
} from "@/lib/api";
import { runOfflineChat } from "@/lib/offline/agent";
import { sessionStore } from "@/lib/offline/store";

export interface TutorChatHandle {
  submit: (text: string) => void;
}

export interface TutorChatProps {
  sessionId: number;
  token: string;
  lessonId?: number;
  isOnline?: boolean;
  onAgentEvent?: (e: AgentEvent) => void;
  onDone?: (e: DoneEvent) => void;
}

const TutorChat = forwardRef<TutorChatHandle, TutorChatProps>(function TutorChat(
  { sessionId, token, lessonId, isOnline = true, onAgentEvent, onDone },
  ref,
) {
  const [turns, setTurns] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const [voiceOn, setVoiceOn] = useState(false);
  const abortRef = useRef<(() => void) | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(
    () => () => {
      abortRef.current?.();
      audioRef.current?.pause();
    },
    [],
  );

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [turns]);

  const playAudio = useCallback((event: AudioEvent) => {
    let url: string | null = null;
    try {
      const binary = atob(event.base64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      const blob = new Blob([bytes], { type: event.mime });
      url = URL.createObjectURL(blob);
    } catch {
      return;
    }

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = "";
      audioRef.current = null;
    }
    const audio = new Audio(url);
    const release = () => {
      if (url) {
        URL.revokeObjectURL(url);
        url = null;
      }
    };
    audio.onended = release;
    audio.onerror = release;
    audioRef.current = audio;
    void audio.play().catch(() => {
      release();
    });
  }, []);

  const fire = useCallback(
    (message: string) => {
      const trimmed = message.trim();
      if (!trimmed || streaming) return;

      const userTurn: Message = { role: "user", text: trimmed };
      const sageTurn: Message = { role: "sage", text: "" };

      setTurns((t) => [...t, userTurn, sageTurn]);
      setDraft("");
      setStreaming(true);
      setActiveAgent("orchestrator:start");

      if (!isOnline && lessonId !== undefined) {
        const historySnapshot = turns.map((t) => ({ role: t.role, text: t.text })) as {
          role: "user" | "sage";
          text: string;
        }[];

        abortRef.current = runOfflineChat(lessonId, sessionId, trimmed, historySnapshot, {
          onAgent: (e: AgentEvent) => {
            setActiveAgent(`${e.agent}:${e.phase}`);
            onAgentEvent?.(e);
          },
          onToken: (e: TokenEvent) =>
            setTurns((t) => {
              const next = [...t];
              const last = next[next.length - 1];
              if (last?.role === "sage") {
                next[next.length - 1] = { ...last, text: last.text + e.text, agent: e.agent };
              }
              return next;
            }),
          onDone: (e: DoneEvent) => {
            setStreaming(false);
            setActiveAgent(null);
            onDone?.(e);
            setTurns((currentTurns) => {
              const lastSage = currentTurns[currentTurns.length - 1];
              if (lastSage?.role === "sage" && lastSage.text) {
                void sessionStore.appendMessage(sessionId, lessonId!, {
                  role: "user",
                  text: trimmed,
                  timestamp: Date.now(),
                });
                void sessionStore.appendMessage(sessionId, lessonId!, {
                  role: "sage",
                  text: lastSage.text,
                  timestamp: Date.now(),
                });
              }
              return currentTurns;
            });
          },
          onError: () => {
            setStreaming(false);
            setActiveAgent(null);
            setTurns((t) => {
              const next = [...t];
              const last = next[next.length - 1];
              if (last?.role === "sage" && !last.text) {
                next[next.length - 1] = {
                  ...last,
                  text: "_(offline model error — the model may still be loading)_",
                };
              }
              return next;
            });
          },
        });
        return;
      }

      abortRef.current = streamTutorChat(
        sessionId,
        trimmed,
        token,
        {
          onAgent: (e: AgentEvent) => {
            setActiveAgent(`${e.agent}:${e.phase}`);
            onAgentEvent?.(e);
          },
          onToken: (e: TokenEvent) =>
            setTurns((t) => {
              const next = [...t];
              const last = next[next.length - 1];
              if (last?.role === "sage") {
                next[next.length - 1] = { ...last, text: last.text + e.text, agent: e.agent };
              }
              return next;
            }),
          onVerification: (v: VerificationEvent) =>
            setTurns((t) => {
              const next = [...t];
              const last = next[next.length - 1];
              if (last?.role === "sage") next[next.length - 1] = { ...last, verification: v };
              return next;
            }),
          onAudio: playAudio,
          onDone: (e: DoneEvent) => {
            setStreaming(false);
            setActiveAgent(null);
            onDone?.(e);
          },
          onError: () => {
            setStreaming(false);
            setActiveAgent(null);
            setTurns((t) => {
              const next = [...t];
              const last = next[next.length - 1];
              if (last?.role === "sage" && !last.text) {
                next[next.length - 1] = {
                  ...last,
                  text: "_(connection error — please try again)_",
                };
              }
              return next;
            });
          },
        },
        { voice: voiceOn },
      );
    },
    [isOnline, lessonId, onAgentEvent, onDone, playAudio, sessionId, streaming, token, turns, voiceOn],
  );

  useImperativeHandle(ref, () => ({ submit: fire }), [fire]);

  return (
    <div className="card flex h-full flex-col p-5">
      <header className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>
            Chat with SAGE
          </h2>
          {!isOnline && (
            <span
              className="rounded-full px-2 py-0.5 text-xs font-semibold"
              style={{
                background: "oklch(85% 0.12 60)",
                color: "oklch(30% 0.12 60)",
                border: "1px solid oklch(70% 0.12 60)",
              }}
            >
              offline
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {isOnline && (
            <button
              type="button"
              onClick={() => setVoiceOn((v) => !v)}
              aria-pressed={voiceOn}
              title="Have SAGE read responses aloud"
              className="rounded-full px-3 py-1 text-xs font-semibold"
              style={{
                background: voiceOn ? "var(--color-primary)" : "var(--color-muted)",
                color: voiceOn ? "var(--color-on-primary)" : "var(--color-primary)",
                border: "1px solid var(--color-border)",
                cursor: "pointer",
              }}
            >
              {voiceOn ? "Voice on" : "Voice off"}
            </button>
          )}
          <AgentBadge active={activeAgent} />
        </div>
      </header>

      <div ref={scrollRef} className="mt-4 flex-1 space-y-3 overflow-y-auto pr-1">
        {turns.map((t, i) => (
          <MessageBubble key={i} msg={t} />
        ))}
        {turns.length === 0 && <EmptyState onPick={(p) => setDraft(p)} isOnline={isOnline} />}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), fire(draft))}
          placeholder={isOnline ? "Type your question…" : "Ask offline — AI running locally…"}
          disabled={streaming}
          className="flex-1 rounded-2xl border px-4 py-3 outline-none focus:ring-2"
          style={{
            borderColor: "var(--color-border)",
            background: "var(--color-muted)",
          }}
        />
        <button
          type="button"
          onClick={() => fire(draft)}
          disabled={streaming || !draft.trim()}
          className="btn-primary disabled:opacity-50"
        >
          {streaming ? "…" : "Ask"}
        </button>
      </div>
    </div>
  );
});

export default TutorChat;

function EmptyState({
  onPick,
  isOnline,
}: {
  onPick: (p: string) => void;
  isOnline: boolean;
}) {
  const prompts = isOnline
    ? [
        "Explain photosynthesis in one paragraph",
        "Quiz me on the concepts I'm weakest at",
        "What should I review before the exam?",
      ]
    : [
        "Can you guide me through this topic?",
        "What is the main idea of this lesson?",
        "Quiz me on what I've learned so far",
      ];

  return (
    <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
      <div
        className="grid h-14 w-14 place-items-center rounded-2xl"
        style={{
          background: isOnline
            ? "linear-gradient(135deg, var(--color-primary), var(--color-accent))"
            : "linear-gradient(135deg, oklch(55% 0.18 50), oklch(45% 0.14 60))",
          color: "white",
          fontFamily: "var(--font-heading)",
          fontSize: 22,
          fontWeight: 700,
          boxShadow: "var(--shadow-md)",
        }}
        aria-hidden
      >
        S
      </div>
      <div>
        <p className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          {isOnline ? "Ask SAGE anything" : "SAGE is running offline"}
        </p>
        <p className="mt-1 text-sm" style={{ color: "var(--color-foreground)", opacity: 0.6 }}>
          {isOnline
            ? "I'll guide you Socratically and cite sources."
            : "Powered by Phi-3.5-mini running in your browser."}
        </p>
      </div>
      <ul className="flex flex-col gap-1.5 text-sm">
        {prompts.map((p) => (
          <li key={p}>
            <button
              type="button"
              onClick={() => onPick(p)}
              className="rounded-full px-3 py-1.5 text-left"
              style={{
                background: "var(--color-muted)",
                color: "var(--color-primary)",
                border: "1px solid var(--color-border)",
                cursor: "pointer",
              }}
            >
              {p}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
