"use client";

import { useCallback, useRef, useState } from "react";

import AgentBadge from "@/components/AgentBadge";
import MessageBubble, { Message } from "@/components/MessageBubble";
import {
  AgentEvent,
  DoneEvent,
  TokenEvent,
  VerificationEvent,
  streamTutorChat,
} from "@/lib/api";

export default function TutorChat({
  sessionId,
  token,
}: {
  sessionId: number;
  token: string;
}) {
  const [turns, setTurns] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const abortRef = useRef<(() => void) | null>(null);

  const send = useCallback(() => {
    const message = draft.trim();
    if (!message || streaming) return;

    setTurns((t) => [...t, { role: "user", text: message }, { role: "sage", text: "" }]);
    setDraft("");
    setStreaming(true);

    abortRef.current = streamTutorChat(sessionId, message, token, {
      onAgent: (e: AgentEvent) => setActiveAgent(`${e.agent}:${e.phase}`),
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
      onDone: (_: DoneEvent) => {
        setStreaming(false);
        setActiveAgent(null);
      },
      onError: () => {
        setStreaming(false);
        setActiveAgent(null);
      },
    });
  }, [draft, sessionId, streaming, token]);

  return (
    <div className="card flex h-full flex-col p-5">
      <header className="flex items-center justify-between">
        <h2 className="text-lg" style={{ fontFamily: "var(--font-heading)" }}>
          Chat with SAGE
        </h2>
        <AgentBadge active={activeAgent} />
      </header>

      <div className="mt-4 flex-1 space-y-3 overflow-y-auto pr-1">
        {turns.map((t, i) => (
          <MessageBubble key={i} msg={t} />
        ))}
        {turns.length === 0 && <EmptyState />}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Type your question…"
          disabled={streaming}
          className="flex-1 rounded-2xl border px-4 py-3 outline-none focus:ring-2"
          style={{
            borderColor: "var(--color-border)",
            background: "var(--color-muted)",
            // @ts-expect-error css var
            "--tw-ring-color": "var(--color-ring)",
          }}
        />
        <button onClick={send} disabled={streaming} className="btn-primary disabled:opacity-50">
          {streaming ? "…" : "Ask"}
        </button>
      </div>
    </div>
  );
}

function EmptyState() {
  const prompts = [
    "Explain photosynthesis in one paragraph",
    "Quiz me on the concepts I'm weakest at",
    "What should I review before the exam?",
  ];
  return (
    <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
      <div
        className="grid h-14 w-14 place-items-center rounded-2xl"
        style={{
          background:
            "linear-gradient(135deg, var(--color-primary), var(--color-accent))",
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
          Ask SAGE anything
        </p>
        <p className="mt-1 text-sm" style={{ color: "var(--color-foreground)", opacity: 0.6 }}>
          I&apos;ll guide you Socratically and cite sources.
        </p>
      </div>
      <ul className="flex flex-col gap-1.5 text-sm">
        {prompts.map((p) => (
          <li
            key={p}
            className="rounded-full px-3 py-1.5"
            style={{
              background: "var(--color-muted)",
              color: "var(--color-primary)",
              border: "1px solid var(--color-border)",
            }}
          >
            {p}
          </li>
        ))}
      </ul>
    </div>
  );
}

