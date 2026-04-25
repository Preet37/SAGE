'use client';
import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/lib/store';

interface Message {
  sender: string;
  content: string;
  timestamp: number;
}

interface Props {
  roomToken: string;
  partnerUsername: string;
  sessionId: number;
  srpInfo?: {
    score: number;
    mastery_delta: number;
    recency_score: number;
    routing_path: string[];
    used_bfs: boolean;
  };
}

export default function PeerChat({ roomToken, partnerUsername, sessionId, srpInfo }: Props) {
  const { token } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sessionEnded, setSessionEnded] = useState(false);
  const [rating, setRating] = useState(0);
  const [ratingNote, setRatingNote] = useState('');
  const [ratingSubmitted, setRatingSubmitted] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/api/network/peer-session/${roomToken}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        setMessages((prev) => [
          ...prev,
          { sender: data.sender ?? 'peer', content: data.content, timestamp: Date.now() },
        ]);
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      } catch {}
    };

    return () => ws.close();
  }, [roomToken]);

  function sendMessage() {
    if (!input.trim() || !wsRef.current) return;
    wsRef.current.send(JSON.stringify({ content: input.trim(), sender: 'me' }));
    setMessages((prev) => [...prev, { sender: 'me', content: input.trim(), timestamp: Date.now() }]);
    setInput('');
  }

  async function submitRating() {
    await fetch(`/api/network/peer-sessions/${sessionId}/rate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ stars: rating, note: ratingNote }),
    });
    setRatingSubmitted(true);
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-green-500/20 bg-green-500/5 overflow-hidden">
      <div className="flex items-center justify-between px-3 py-2 border-b border-green-500/10">
        <div>
          <span className="text-xs font-semibold text-t0">Peer: {partnerUsername}</span>
          {srpInfo && (
            <div className="text-[9px] text-green-400 mt-0.5">
              SRP score: {srpInfo.score.toFixed(2)}
              {srpInfo.used_bfs && ` · routed via ${srpInfo.routing_path.join(' → ')}`}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
            arista
          </span>
          <button
            onClick={() => setSessionEnded(true)}
            className="text-[9px] text-t3 hover:text-t0 px-2 py-0.5 rounded border border-white/10"
          >
            End
          </button>
        </div>
      </div>

      {srpInfo && (
        <div className="px-3 py-2 bg-green-500/5 border-b border-green-500/10 text-[9px] text-t3 flex gap-3">
          <span>Mastery Δ: {srpInfo.mastery_delta.toFixed(2)}</span>
          <span>Recency: {srpInfo.recency_score.toFixed(2)}</span>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === 'me' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-xl px-3 py-2 text-xs ${
                msg.sender === 'me'
                  ? 'bg-green-600/30 text-t0'
                  : 'bg-bg2 border border-white/5 text-t0'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {sessionEnded && !ratingSubmitted && (
        <div className="p-4 border-t border-white/5 bg-bg1">
          <p className="text-xs text-t0 font-semibold mb-2">Rate this peer session</p>
          <div className="flex gap-1 mb-2">
            {[1, 2, 3, 4, 5].map((s) => (
              <button
                key={s}
                onClick={() => setRating(s)}
                className={`text-xl ${s <= rating ? 'text-yellow-400' : 'text-t3'}`}
              >
                ★
              </button>
            ))}
          </div>
          <textarea
            value={ratingNote}
            onChange={(e) => setRatingNote(e.target.value)}
            placeholder="Optional note…"
            className="w-full bg-bg2 border border-white/10 rounded-lg px-2 py-1.5 text-xs text-t0 resize-none h-12 mb-2"
          />
          <button
            onClick={submitRating}
            disabled={rating === 0}
            className="w-full py-1.5 rounded-lg bg-green-600/30 text-green-400 text-xs font-semibold disabled:opacity-40"
          >
            Submit rating
          </button>
        </div>
      )}

      {ratingSubmitted && (
        <div className="p-3 text-center text-xs text-green-400 border-t border-white/5">
          ✓ Rating submitted — helps SRP improve future matches
        </div>
      )}

      {!sessionEnded && (
        <div className="flex gap-2 p-3 border-t border-white/5">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Message your peer…"
            className="flex-1 bg-bg2 border border-white/10 rounded-full px-3 py-1.5 text-xs text-t0"
          />
          <button
            onClick={sendMessage}
            className="w-8 h-8 rounded-full bg-green-600/30 text-green-400 font-bold text-sm"
          >
            ↑
          </button>
        </div>
      )}
    </div>
  );
}
