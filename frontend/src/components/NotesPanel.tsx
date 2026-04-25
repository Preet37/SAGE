"use client";

import { useCallback, useEffect, useState } from "react";

import { getNotes, reviseNotes, type Notes } from "@/lib/api";

interface NotesPanelProps {
  sessionId: number;
  token: string;
}

const LOCAL_KEY = (sid: number) => `sage-notes-${sid}`;

export default function NotesPanel({ sessionId, token }: NotesPanelProps) {
  const [tab, setTab] = useState<"summary" | "write">("summary");
  const [notes, setNotes] = useState<Notes | null>(null);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    if (!token) return;
    getNotes(sessionId, token)
      .then(setNotes)
      .catch((err) => setError(String(err)));
  }, [sessionId, token]);

  useEffect(() => {
    refresh();
    const cached = typeof window !== "undefined" ? window.localStorage.getItem(LOCAL_KEY(sessionId)) : null;
    if (cached) setText(cached);
  }, [refresh, sessionId]);

  const onRevise = useCallback(async () => {
    if (!token || !text.trim()) return;
    setBusy(true);
    setError(null);
    try {
      const result = await reviseNotes(sessionId, text, token);
      setNotes(result);
      window.localStorage.setItem(LOCAL_KEY(sessionId), text);
      setTab("summary");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to revise notes");
    } finally {
      setBusy(false);
    }
  }, [sessionId, text, token]);

  const onDownload = useCallback(() => {
    if (!notes) return;
    const blob = new Blob([notes.markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `sage-session-${sessionId}.md`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }, [notes, sessionId]);

  return (
    <div className="card flex h-full flex-col p-5">
      <header className="flex items-center justify-between">
        <h3 className="text-base" style={{ fontFamily: "var(--font-heading)", fontWeight: 600 }}>
          Notes
        </h3>
        <div className="flex gap-1 text-xs">
          {(["summary", "write"] as const).map((id) => (
            <button
              key={id}
              type="button"
              onClick={() => setTab(id)}
              className="rounded-full px-3 py-1 font-semibold"
              style={{
                background: tab === id ? "var(--color-primary)" : "var(--color-muted)",
                color: tab === id ? "var(--color-on-primary)" : "var(--color-primary)",
                border: "1px solid var(--color-border)",
                cursor: "pointer",
              }}
            >
              {id === "summary" ? "Summary" : "Write"}
            </button>
          ))}
        </div>
      </header>

      {error && (
        <p role="alert" className="mt-2 text-xs" style={{ color: "var(--color-destructive)" }}>
          {error}
        </p>
      )}

      <div className="mt-3 flex-1 overflow-auto pr-1 text-sm">
        {tab === "summary" ? (
          <SummaryView notes={notes} />
        ) : (
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write your own notes; SAGE will highlight gaps."
            className="h-full w-full resize-none rounded-2xl border bg-white px-3 py-2 text-sm"
            style={{ borderColor: "var(--color-border)" }}
          />
        )}
      </div>

      <footer className="mt-3 flex justify-between gap-2">
        <button
          type="button"
          onClick={onDownload}
          disabled={!notes}
          className="rounded-full px-3 py-1.5 text-xs font-semibold disabled:opacity-50"
          style={{
            background: "var(--color-muted)",
            color: "var(--color-primary)",
            border: "1px solid var(--color-border)",
            cursor: "pointer",
          }}
        >
          Download .md
        </button>
        {tab === "write" && (
          <button
            type="button"
            onClick={onRevise}
            disabled={busy || !text.trim()}
            className="btn-primary text-xs"
          >
            {busy ? "Reviewing…" : "Review with SAGE"}
          </button>
        )}
      </footer>
    </div>
  );
}

function SummaryView({ notes }: { notes: Notes | null }) {
  if (!notes) {
    return (
      <div className="space-y-2">
        <div className="h-3 w-5/6 rounded-full shimmer" style={{ background: "var(--color-muted)" }} />
        <div className="h-3 w-3/4 rounded-full shimmer" style={{ background: "var(--color-muted)" }} />
        <div className="h-3 w-2/3 rounded-full shimmer" style={{ background: "var(--color-muted)" }} />
      </div>
    );
  }
  return (
    <div className="space-y-3">
      <p className="text-xs opacity-70">{notes.summary}</p>
      <pre className="whitespace-pre-wrap rounded-xl bg-transparent text-xs leading-relaxed">
        {notes.markdown}
      </pre>
      {notes.suggestions.length > 0 && (
        <div className="rounded-xl p-3" style={{ background: "var(--color-muted)" }}>
          <p className="text-xs font-semibold">Next steps</p>
          <ul className="mt-1 list-disc pl-4 text-xs">
            {notes.suggestions.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
