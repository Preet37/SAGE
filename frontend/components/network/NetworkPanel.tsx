'use client';
import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/lib/store';
import { requestPeerMatch, getNetworkStatus, getPeerSocketUrl, getTopology } from '@/lib/api';
import NetworkTopology from './NetworkTopology';
import RoutingTable from './RoutingTable';

interface Props { lessonId: number }
interface NetworkStatus { active_students: number; hot_concepts: { concept: string; students_waiting: number; concept_id: number }[]; peer_sessions: number }
interface TopologyData {
  nodes: { id: string; label: string; kind: 'self' | 'tutor' | 'co_learner'; score?: number }[];
  edges: { source: string; target: string; weight: number }[];
  weights: Record<string, number>;
  routing_table: {
    user_id: number; display: string; score: number;
    components: { mastery_delta: number; recency: number; style_compat: number; novelty: number };
    role: string; last_seen_seconds: number;
  }[];
}

export default function NetworkPanel({ lessonId }: Props) {
  const { token } = useAuthStore();
  const [status, setStatus] = useState<NetworkStatus | null>(null);
  const [matchResult, setMatchResult] = useState<unknown | null>(null);
  const [topology, setTopology] = useState<TopologyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState(false);
  const [roomMessages, setRoomMessages] = useState<{ mine: boolean; text: string; ts: number }[]>([]);
  const [draft, setDraft] = useState('');
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

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
      const [result, topo] = await Promise.all([
        requestPeerMatch(token, conceptId, lessonId),
        getTopology(token, conceptId).catch(() => null),
      ]);
      setMatchResult(result);
      if (topo) setTopology(topo);
      const roomToken = (result as Record<string, unknown>).room_token as string | undefined;
      if (roomToken) connectRoom(roomToken);
    } catch {
      // swallow — UI already shows match state
    } finally {
      setMatching(false);
    }
  }

  function connectRoom(roomToken: string) {
    socketRef.current?.close();
    setRoomMessages([]);
    const socket = new WebSocket(getPeerSocketUrl(roomToken));
    socketRef.current = socket;
    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onerror = () => setConnected(false);
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setRoomMessages((m) => [...m, { mine: false, text: String(data.text || ''), ts: Date.now() }]);
      } catch {
        setRoomMessages((m) => [...m, { mine: false, text: String(event.data), ts: Date.now() }]);
      }
    };
  }

  function sendRoomMessage() {
    const text = draft.trim();
    if (!text || !socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;
    socketRef.current.send(JSON.stringify({ text, sent_at: new Date().toISOString() }));
    setRoomMessages((m) => [...m, { mine: true, text, ts: Date.now() }]);
    setDraft('');
  }

  useEffect(() => () => socketRef.current?.close(), []);

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
              <div className="mt-4 border border-white/5 rounded-xl overflow-hidden bg-bg3">
                <div className="px-3 py-2 border-b border-white/5 flex items-center gap-2">
                  <span className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-grn' : 'bg-ora'}`} />
                  <span className="text-[10px] font-bold uppercase tracking-widest text-t3">
                    Peer Room
                  </span>
                </div>
                <div className="h-40 overflow-y-auto p-3 space-y-2">
                  {roomMessages.length === 0 ? (
                    <div className="text-xs text-t3">No messages yet.</div>
                  ) : roomMessages.map((msg) => (
                    <div key={msg.ts} className={`text-xs rounded-lg px-3 py-2 max-w-[85%] ${
                      msg.mine ? 'ml-auto bg-acc/20 text-t0' : 'bg-bg2 text-t1'
                    }`}>
                      {msg.text}
                    </div>
                  ))}
                </div>
                <div className="p-2 border-t border-white/5 flex gap-2">
                  <input
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') sendRoomMessage(); }}
                    disabled={!connected}
                    className="flex-1 bg-bg2 border border-white/5 rounded-lg px-3 py-2 text-xs text-t0 outline-none focus:border-acc/30 disabled:opacity-50"
                    placeholder={connected ? 'Message your peer…' : 'Connecting…'}
                  />
                  <button
                    onClick={sendRoomMessage}
                    disabled={!connected || !draft.trim()}
                    className="text-[10px] font-bold px-3 py-2 bg-acc text-white rounded-lg disabled:opacity-50"
                  >
                    Send
                  </button>
                </div>
              </div>
            </>
          ) : (
            <p className="text-xs text-t1">You've been added to the queue for <strong>{mr.concept as string}</strong>. SAGE will notify you when a match is found.</p>
          )}
        </div>
      )}

      {/* SRP Topology visualization */}
      {topology && topology.routing_table.length > 0 && (
        <div className="mt-6 space-y-3">
          <div className="flex items-center gap-2">
            <div className="text-[10px] font-bold uppercase tracking-widest text-ora">SRP Topology</div>
            <span className="text-[9px] text-t3 font-mono ml-auto">
              srp = 0.4·Δm + 0.2·rec + 0.2·style + 0.2·novel
            </span>
          </div>
          <NetworkTopology nodes={topology.nodes} edges={topology.edges} />
          <RoutingTable
            rows={topology.routing_table}
            weights={topology.weights}
            selectedUserId={(matchResult as { selected?: { user_id: number } } | null)?.selected?.user_id}
          />
        </div>
      )}

      {!topology && (
        <div className="mt-6 bg-bg2 border border-ora/15 rounded-2xl p-4">
          <div className="text-[10px] font-bold uppercase tracking-widest text-ora mb-2">SAGE Routing Protocol</div>
          <p className="text-[11px] text-t1 leading-relaxed">
            Tap <strong>Join</strong> on a hot concept to compute the routing table.
            SRP scores each peer on mastery delta, recency, style compatibility, and
            novelty — like Arista's fabric routes packets, SAGE routes <em>students</em>
            to the best learning partner.
          </p>
        </div>
      )}
    </div>
  );
}
