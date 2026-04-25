"use client";

import { useEffect, useState } from "react";

import { getReplay, type ReplaySession } from "@/lib/api";

interface ReplayPanelProps {
  sessionId: number;
  token: string;
  refreshKey?: number;
}

export default function ReplayPanel({ sessionId, token, refreshKey = 0 }: ReplayPanelProps) {
  const [data, setData] = useState<ReplaySession | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    getReplay(sessionId, token)
      .then(setData)
      .catch((err) => setError(String(err)));
  }, [sessionId, token, refreshKey]);

  const turns = parseTurns(data?.transcript ?? "");

  return (
    <div className="card flex h-full flex-col p-5">
      <header>
        <h3 className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          Replay
        </h3>
        <p className="mt-1 text-xs opacity-70">
          {data
            ? `Started ${new Date(data.started_at).toLocaleString()} · ${turns.length} turn(s)`
            : "Loading…"}
        </p>
      </header>

      {error && (
        <p role="alert" className="mt-2 text-xs" style={{ color: "var(--color-destructive)" }}>
          {error}
        </p>
      )}

      <ol className="mt-3 flex-1 space-y-2 overflow-auto pr-1 text-sm">
        {turns.length === 0 && (
          <li className="rounded-2xl px-3 py-2 text-xs opacity-70" style={{ background: "var(--color-muted)" }}>
            No turns yet — ask SAGE something to populate this view.
          </li>
        )}
        {turns.map((t, i) => (
          <li key={i} className="rounded-2xl border p-3" style={{ borderColor: "var(--color-border)" }}>
            <p className="text-xs font-semibold opacity-70">
              {t.role === "user" ? "You" : "SAGE"}
            </p>
            <p className="mt-1 whitespace-pre-wrap">{t.text}</p>
          </li>
        ))}
      </ol>
    </div>
  );
}

interface ReplayTurn {
  role: "user" | "sage";
  text: string;
}

function parseTurns(transcript: string): ReplayTurn[] {
  const out: ReplayTurn[] = [];
  let role: ReplayTurn["role"] | null = null;
  let buf: string[] = [];
  for (const line of transcript.split("\n")) {
    if (line.startsWith("USER:")) {
      flush();
      role = "user";
      buf = [line.slice(5).trim()];
    } else if (line.startsWith("SAGE:")) {
      flush();
      role = "sage";
      buf = [line.slice(5).trim()];
    } else if (role) {
      buf.push(line);
    }
  }
  flush();
  return out;

  function flush(): void {
    if (role && buf.length) out.push({ role, text: buf.join("\n").trim() });
  }
}
