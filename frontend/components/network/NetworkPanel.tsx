'use client';
import { useState, useEffect } from 'react';
import { useAuthStore } from '@/lib/store';
import { requestPeerMatch, getNetworkStatus } from '@/lib/api';

interface Props { lessonId: number }
interface NetworkStatus { active_students: number; hot_concepts: { concept: string; students_waiting: number; concept_id: number }[]; peer_sessions: number }

export default function NetworkPanel({ lessonId }: Props) {
  const { token } = useAuthStore();
  const [status, setStatus] = useState<NetworkStatus | null>(null);
  const [matchResult, setMatchResult] = useState<unknown | null>(null);
  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState(false);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  async function loadStatus() {
    try {
      const s = await getNetworkStatus();
      setStatus(s);
    } catch {}
    setLoading(false);
  }

  async function handlePeerMatch(conceptId: number) {
    if (!token) return;
    setMatching(true);
    try {
      const result = await requestPeerMatch(token, conceptId, lessonId);
      setMatchResult(result);
    } catch (e) {
      console.error(e);
    } finally {
      setMatching(false);
    }
  }

  if (loading) return <div className="p-6 text-t2 text-sm">Loading network…</div>;

  const s = status as NetworkStatus;
  const mr = matchResult as Record<string, unknown> | null;

  return (
    <div className="p-6 h-full overflow-y-auto">
      <div className="text-[9.5px] font-bold uppercase tracking-widest text-t3 mb-6">Student Network · Arista Track</div>

      {/* Network stats */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        {[
          { label: 'Active Students', value: s?.active_students ?? 0, color: 'text-acc' },
          { label: 'Hot Topics', value: s?.hot_concepts?.length ?? 0, color: 'text-ora' },
          { label: 'Live Pairs', value: s?.peer_sessions ?? 0, color: 'text-grn' },
        ].map(stat => (
          <div key={stat.label} className="bg-bg2 border border-white/5 rounded-2xl p-4 text-center">
            <div className={`text-2xl font-black mb-1 ${stat.color}`}>{stat.value}</div>
            <div className="text-[10px] text-t3 font-medium">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Hot concepts */}
      <div className="mb-6">
        <div className="text-[10px] font-bold uppercase tracking-widest text-t3 mb-3">Hot Right Now</div>
        {s?.hot_concepts?.length ? (
          <div className="space-y-2">
            {s.hot_concepts.map(c => (
              <div key={c.concept_id} className="flex items-center gap-3 bg-bg2 border border-white/5 rounded-xl p-3">
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-t0 truncate">{c.concept}</div>
                  <div className="text-[10px] text-t2">{c.students_waiting} student(s) waiting</div>
                </div>
                <button
                  onClick={() => handlePeerMatch(c.concept_id)}
                  disabled={matching}
                  className="text-[10px] font-bold px-3 py-1.5 bg-acc/15 text-acc border border-acc/25 rounded-lg hover:bg-acc/25 transition-all disabled:opacity-50"
                >
                  {matching ? '…' : 'Join'}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-bg2 border border-white/5 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">◉</div>
            <div className="text-xs text-t2">No one waiting yet.</div>
            <div className="text-[10px] text-t3 mt-1">Be the first to request a peer.</div>
          </div>
        )}
      </div>

      {/* Match result */}
      {mr && (
        <div className={`rounded-2xl border p-4 ${mr.matched ? 'border-grn/30 bg-grn/5' : 'border-acc/20 bg-acc/5'}`}>
          <div className={`text-sm font-bold mb-1 ${mr.matched ? 'text-grn' : 'text-acc'}`}>
            {mr.matched ? '⚡ Match Found!' : '◉ Waiting for Peer'}
          </div>
          {mr.matched ? (
            <>
              <p className="text-xs text-t1 mb-3">Connected on: <strong>{mr.concept as string}</strong></p>
              <div className="bg-bg3 rounded-xl p-3 font-mono text-[10px] text-t2">
                room: {mr.room_token as string}<br />
                peer_is_master: {String(mr.partner_is_master as boolean)}
              </div>
            </>
          ) : (
            <p className="text-xs text-t1">You've been added to the queue for <strong>{mr.concept as string}</strong>. SAGE will notify you when a match is found.</p>
          )}
        </div>
      )}

      {/* Network visualization description */}
      <div className="mt-6 bg-bg2 border border-ora/15 rounded-2xl p-4">
        <div className="text-[10px] font-bold uppercase tracking-widest text-ora mb-2">Arista Routing</div>
        <p className="text-[11px] text-t1 leading-relaxed">
          Peer matching uses concept-similarity scoring to route students to the most relevant peers — 
          like Arista's network fabric routes packets to optimal paths. Students who've mastered a concept 
          are preferred as "tutor peers" over co-learners.
        </p>
      </div>
    </div>
  );
}
