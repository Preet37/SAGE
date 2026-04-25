'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { getSessionReplay, getSessions } from '@/lib/api';

interface SessionSummary {
  id: number;
  lesson_id: number;
  teaching_mode: string;
  started_at: string;
}

interface ReplayTurn {
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  agent_trace?: Record<string, unknown>;
  verification?: { passed: boolean; flags: string[] };
  retrieved_chunks_preview?: string[];
}

interface ReplayData {
  session_id: number;
  teaching_mode: string;
  turns: ReplayTurn[];
  agent_decisions?: Record<string, unknown>[];
}

export default function ReplayPanel({ activeSessionId }: { activeSessionId: number | null }) {
  const { token } = useAuthStore();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(activeSessionId);
  const [replay, setReplay] = useState<ReplayData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) return;
    let cancelled = false;
    setLoading(true);
    getSessions(token)
      .then((rows) => {
        if (cancelled) return;
        setSessions(rows);
        setSelectedId(activeSessionId || rows[0]?.id || null);
      })
      .catch((e) => !cancelled && setError(String(e)))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, [token, activeSessionId]);

  useEffect(() => {
    if (!token || !selectedId) return;
    let cancelled = false;
    setError('');
    getSessionReplay(token, selectedId)
      .then((data) => !cancelled && setReplay(data))
      .catch((e) => !cancelled && setError(String(e)));
    return () => { cancelled = true; };
  }, [token, selectedId]);

  if (loading) return <div className="p-6 text-t2 text-sm">Loading replay…</div>;

  return (
    <div className="h-full overflow-hidden grid grid-cols-[220px_1fr]">
      <aside className="border-r border-white/5 bg-bg1 overflow-y-auto p-3">
        <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Sessions</div>
        {sessions.length === 0 ? (
          <div className="text-xs text-t2 bg-bg2 border border-white/5 rounded-xl p-3">
            No completed tutor turns yet.
          </div>
        ) : sessions.map((s) => (
          <button
            key={s.id}
            onClick={() => setSelectedId(s.id)}
            className={`w-full text-left rounded-xl border p-3 mb-2 transition-all ${
              selectedId === s.id ? 'bg-acc/10 border-acc/30 text-t0' : 'bg-bg2 border-white/5 text-t2 hover:text-t0'
            }`}
          >
            <div className="text-xs font-semibold">Session {s.id}</div>
            <div className="text-[10px] text-t3 mt-1">{new Date(s.started_at).toLocaleString()}</div>
            <div className="text-[10px] text-t3 mt-1">Mode: {s.teaching_mode}</div>
          </button>
        ))}
      </aside>

      <main className="overflow-y-auto p-6">
        {error && <div className="mb-4 text-xs text-red-300 bg-red-500/10 border border-red-500/20 rounded-xl p-3">{error}</div>}
        {!replay ? (
          <div className="text-sm text-t2">Select a session to inspect its audit trail.</div>
        ) : (
          <div className="space-y-4">
            <div>
              <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-1">Replay Audit</div>
              <h2 className="text-xl font-bold text-t0">Session {replay.session_id}</h2>
            </div>

            {replay.turns.length === 0 ? (
              <div className="text-sm text-t2 bg-bg2 border border-white/5 rounded-xl p-4">
                This session has no persisted messages yet. Send a tutor message, then return here.
              </div>
            ) : replay.turns.map((turn, index) => (
              <article key={`${turn.created_at}-${index}`} className="bg-bg2 border border-white/5 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-[10px] font-bold uppercase tracking-wider ${turn.role === 'assistant' ? 'text-acc' : 'text-t2'}`}>
                    {turn.role}
                  </span>
                  <span className="text-[10px] text-t3">{new Date(turn.created_at).toLocaleTimeString()}</span>
                  {turn.verification && (
                    <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      turn.verification.passed ? 'text-grn bg-grn/10' : 'text-ora bg-ora/10'
                    }`}>
                      {turn.verification.passed ? 'Verified' : 'Flagged'}
                    </span>
                  )}
                </div>
                <p className="text-sm text-t1 whitespace-pre-wrap leading-relaxed">{turn.content}</p>
                {!!turn.retrieved_chunks_preview?.length && (
                  <div className="mt-3 text-[10px] text-t3 border-t border-white/5 pt-3">
                    Retrieved: {turn.retrieved_chunks_preview.join(' / ')}
                  </div>
                )}
                {!!turn.agent_trace?.events && (
                  <div className="mt-3 grid grid-cols-2 gap-2">
                    {(turn.agent_trace.events as Record<string, unknown>[]).map((event) => (
                      <div key={event.type as string} className="bg-bg3 rounded-lg px-2 py-1.5 text-[10px] text-t2">
                        {event.type as string}
                      </div>
                    ))}
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
