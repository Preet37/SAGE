"use client";

import { useEffect, useRef, useState } from "react";
import { getToken } from "./auth";
import { api, PeerOut, PresenceResponse } from "./api";
import { API_URL } from "./api";

interface NudgeEvent {
  type: "nudge";
  from: string;
  to: string;
  message: string;
  ts: string;
}

interface SnapshotEvent {
  type: "snapshot" | "presence";
  peers: PeerOut[];
  actor?: string;
}

type WsEvent = NudgeEvent | SnapshotEvent;

interface UsePresenceOptions {
  lessonId?: string | null;
  status?: string;
  note?: string;
  lookingForPair?: boolean;
  displayName?: string;
  enabled?: boolean;
}

export function usePresence(opts: UsePresenceOptions = {}) {
  const { lessonId, status = "studying", note = "", lookingForPair = false, displayName, enabled = true } = opts;
  const [presence, setPresence] = useState<PresenceResponse | null>(null);
  const [livePeers, setLivePeers] = useState<PeerOut[]>([]);
  const [nudges, setNudges] = useState<NudgeEvent[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const heartbeatRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!enabled) return;
    const token = getToken();
    if (!token) return;
    let cancelled = false;

    async function tick() {
      try {
        const data = await api.network.heartbeat({
          lesson_id: lessonId ?? null,
          status, note,
          looking_for_pair: lookingForPair,
          display_name: displayName,
        }, token!);
        if (!cancelled) setPresence(data);
      } catch { /* ignore transient errors */ }
    }

    tick();
    heartbeatRef.current = setInterval(tick, 30_000);

    return () => {
      cancelled = true;
      if (heartbeatRef.current) clearInterval(heartbeatRef.current);
      api.network.leave(token!).catch(() => {});
    };
  }, [enabled, lessonId, status, note, lookingForPair, displayName]);

  useEffect(() => {
    if (!enabled) return;
    const token = getToken();
    if (!token) return;
    const wsUrl = API_URL.replace(/^http/, "ws") + "/network/ws";
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data) as WsEvent;
        if (data.type === "snapshot" || data.type === "presence") {
          setLivePeers((data as SnapshotEvent).peers || []);
        } else if (data.type === "nudge") {
          setNudges((prev) => [data, ...prev].slice(0, 10));
        }
      } catch { /* ignore */ }
    };

    return () => {
      try { ws.close(); } catch { /* ignore */ }
      wsRef.current = null;
    };
  }, [enabled]);

  function nudge(toUserId: string, message: string) {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    const me = presence?.me.user_id || "";
    ws.send(JSON.stringify({ type: "nudge", from: me, to: toUserId, message }));
  }

  return { presence, livePeers, nudges, nudge, dismissNudge: (ts: string) => setNudges((p) => p.filter((n) => n.ts !== ts)) };
}
