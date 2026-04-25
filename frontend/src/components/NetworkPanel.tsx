"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import {
  networkStatus,
  openPeerSocket,
  requestPeerMatch,
  type NetworkStatus,
  type PeerMatch,
} from "@/lib/api";

interface NetworkPanelProps {
  token: string;
  lessonId: number | null;
}

interface RoomMessage {
  from: "you" | "peer";
  text: string;
  at: number;
}

const POLL_MS = 10_000;

export default function NetworkPanel({ token, lessonId }: NetworkPanelProps) {
  const [status, setStatus] = useState<NetworkStatus | null>(null);
  const [match, setMatch] = useState<PeerMatch | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [conceptInput, setConceptInput] = useState("");
  const [messages, setMessages] = useState<RoomMessage[]>([]);
  const [draft, setDraft] = useState("");
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let cancelled = false;
    const tick = () => {
      networkStatus(token)
        .then((s) => !cancelled && setStatus(s))
        .catch(() => {});
    };
    tick();
    const id = setInterval(tick, POLL_MS);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [token]);

  // Open the WS once we are matched and there is a room token.
  useEffect(() => {
    if (!match || match.state !== "matched") return;
    const ws = openPeerSocket(match.room_token, token);
    wsRef.current = ws;
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data) as { event?: string; text?: string };
        if (data.event === "message" && typeof data.text === "string") {
          setMessages((m) => [...m, { from: "peer", text: data.text!, at: Date.now() }]);
        }
      } catch {
        /* ignore */
      }
    };
    ws.onclose = () => {
      if (wsRef.current === ws) wsRef.current = null;
    };
    return () => {
      ws.close();
      if (wsRef.current === ws) wsRef.current = null;
    };
  }, [match]);

  const onMatch = useCallback(
    async (concept?: string) => {
      setBusy(true);
      setError(null);
      try {
        const result = await requestPeerMatch(token, {
          concept: concept ?? null,
          lesson_id: lessonId,
        });
        setMatch(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Match failed");
      } finally {
        setBusy(false);
      }
    },
    [lessonId, token],
  );

  const onSend = useCallback(() => {
    if (!wsRef.current || !draft.trim()) return;
    const text = draft.trim();
    wsRef.current.send(JSON.stringify({ text }));
    setMessages((m) => [...m, { from: "you", text, at: Date.now() }]);
    setDraft("");
  }, [draft]);

  return (
    <div className="card flex h-full flex-col p-5">
      <header className="flex items-center justify-between">
        <h3 className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          Network
        </h3>
        <div className="flex gap-2 text-xs opacity-70">
          <Tag label={`${status?.waiting ?? 0} waiting`} />
          <Tag label={`${status?.active_rooms ?? 0} live`} />
        </div>
      </header>

      <p className="mt-1 text-xs opacity-70">
        Find a peer studying the same concept and chat in real time.
      </p>

      {!match && (
        <div className="mt-3 space-y-3">
          <div className="flex gap-2">
            <input
              value={conceptInput}
              onChange={(e) => setConceptInput(e.target.value)}
              placeholder="Concept (optional)"
              className="flex-1 rounded-xl border bg-white px-3 py-2 text-sm"
              style={{ borderColor: "var(--color-border)" }}
            />
            <button
              type="button"
              onClick={() => onMatch(conceptInput.trim() || undefined)}
              disabled={busy}
              className="btn-primary text-xs"
            >
              {busy ? "Matching…" : "Find peer"}
            </button>
          </div>
          {(status?.hot_concepts.length ?? 0) > 0 && (
            <div>
              <p className="text-xs font-semibold opacity-70">Hot right now</p>
              <ul className="mt-1 flex flex-wrap gap-1.5">
                {status?.hot_concepts.map((c) => (
                  <li key={c}>
                    <button
                      type="button"
                      onClick={() => onMatch(c)}
                      className="rounded-full px-2.5 py-1 text-xs font-semibold"
                      style={{
                        background: "var(--color-muted)",
                        color: "var(--color-primary)",
                        border: "1px solid var(--color-border)",
                        cursor: "pointer",
                      }}
                    >
                      {c}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {match && (
        <div className="mt-3 flex flex-1 flex-col">
          <div
            className="rounded-2xl px-3 py-2 text-xs"
            style={{
              background: match.state === "matched" ? "var(--color-secondary)" : "var(--color-muted)",
              color: match.state === "matched" ? "white" : "var(--color-foreground)",
            }}
          >
            {match.state === "matched"
              ? `Matched with ${match.peer ?? "a peer"} · room ${match.room_token}`
              : `Waiting for a peer · token ${match.room_token}`}
          </div>

          {match.state === "matched" && (
            <>
              <div className="mt-2 flex-1 space-y-1.5 overflow-auto pr-1 text-sm">
                {messages.length === 0 && (
                  <p className="text-xs opacity-60">Say hi 👋</p>
                )}
                {messages.map((m, i) => (
                  <div
                    key={i}
                    className={`max-w-[80%] rounded-2xl px-3 py-1.5 text-xs ${
                      m.from === "you" ? "ml-auto" : "mr-auto"
                    }`}
                    style={{
                      background: m.from === "you" ? "var(--color-primary)" : "var(--color-muted)",
                      color: m.from === "you" ? "var(--color-on-primary)" : "var(--color-foreground)",
                    }}
                  >
                    {m.text}
                  </div>
                ))}
              </div>
              <div className="mt-2 flex gap-2">
                <input
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && onSend()}
                  placeholder="Message your peer…"
                  className="flex-1 rounded-xl border bg-white px-3 py-2 text-sm"
                  style={{ borderColor: "var(--color-border)" }}
                />
                <button type="button" onClick={onSend} className="btn-primary text-xs">
                  Send
                </button>
              </div>
            </>
          )}

          <button
            type="button"
            onClick={() => {
              setMatch(null);
              setMessages([]);
            }}
            className="mt-2 self-end text-xs opacity-60 hover:opacity-100"
          >
            Leave room
          </button>
        </div>
      )}

      {error && (
        <p role="alert" className="mt-2 text-xs" style={{ color: "var(--color-destructive)" }}>
          {error}
        </p>
      )}
    </div>
  );
}

function Tag({ label }: { label: string }) {
  return (
    <span
      className="rounded-full px-2 py-0.5 font-semibold"
      style={{ background: "var(--color-muted)", border: "1px solid var(--color-border)" }}
    >
      {label}
    </span>
  );
}
