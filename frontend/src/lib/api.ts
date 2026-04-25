export const API_BASE = "/api";

export type AgentEvent = {
  agent: "orchestrator" | "retriever" | "socratic" | "pedagogy" | "content" |
         "concept_map" | "assessment" | "peer_match" | "progress" | "verifier";
  phase: "start" | "retrieved" | "generating" | "verifying" | "done";
  k?: number;
  scores?: number[];
  system_prompt_chars?: number;
  plan?: Record<string, unknown>;
  delta?: unknown;
  data?: unknown;
  peers?: unknown;
  trace_id?: string;
  session_id?: number;
};

export type TokenEvent  = { agent: "socratic"; text: string };
export type ClaimVerdict = {
  claim: string; score: number; grounded: boolean; source_index: number | null;
};
export type VerificationEvent = {
  score: number; grounded: boolean; claims: ClaimVerdict[];
};
export type DoneEvent = { session_id: number; ok: boolean; grounded: boolean };

export type SSEHandlers = {
  onAgent?: (e: AgentEvent) => void;
  onToken?: (e: TokenEvent) => void;
  onVerification?: (e: VerificationEvent) => void;
  onDone?: (e: DoneEvent) => void;
  onError?: (err: unknown) => void;
};

export function streamTutorChat(
  sessionId: number,
  message: string,
  token: string,
  handlers: SSEHandlers,
): () => void {
  const ctl = new AbortController();
  const url = `${API_BASE}/tutor/chat?session_id=${sessionId}&message=${encodeURIComponent(message)}`;

  (async () => {
    try {
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}`, Accept: "text/event-stream" },
        signal: ctl.signal,
      });
      if (!res.ok || !res.body) throw new Error(`SSE ${res.status}`);

      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });

        let idx: number;
        while ((idx = buf.indexOf("\n\n")) !== -1) {
          const block = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          dispatchSSEBlock(block, handlers);
        }
      }
    } catch (err) {
      if (!ctl.signal.aborted) handlers.onError?.(err);
    }
  })();

  return () => ctl.abort();
}

function dispatchSSEBlock(block: string, h: SSEHandlers) {
  let event = "message";
  const dataLines: string[] = [];
  for (const line of block.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  if (!dataLines.length) return;
  let data: unknown;
  try { data = JSON.parse(dataLines.join("\n")); } catch { return; }

  switch (event) {
    case "agent_event":  h.onAgent?.(data as AgentEvent); break;
    case "token":        h.onToken?.(data as TokenEvent); break;
    case "verification": h.onVerification?.(data as VerificationEvent); break;
    case "done":         h.onDone?.(data as DoneEvent); break;
  }
}
