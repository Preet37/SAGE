"use client";
import { useCallback, useRef } from "react";
import { getToken } from "./auth";
import { API_URL } from "./api";

function uid(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  const buf = new Uint8Array(16);
  crypto.getRandomValues(buf);
  buf[6] = (buf[6] & 0x0f) | 0x40;
  buf[8] = (buf[8] & 0x3f) | 0x80;
  const hex = Array.from(buf, (b) => b.toString(16).padStart(2, "0")).join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

export { uid };

function parseSSEBuffer(buffer: string): { events: unknown[]; remainder: string } {
  const events: unknown[] = [];
  const parts = buffer.split("\n\n");
  const remainder = parts.pop() ?? "";
  for (const part of parts) {
    for (const line of part.split("\n")) {
      if (line.startsWith("data: ")) {
        try {
          events.push(JSON.parse(line.slice(6)));
        } catch {
          /* ignore malformed */
        }
      }
    }
  }
  return { events, remainder };
}

export interface SSEEvent {
  type: string;
  [key: string]: unknown;
}

/**
 * Stream an SSE endpoint and call onEvent for each parsed event.
 * Returns an AbortController so the caller can cancel.
 */
export function streamSSE(
  path: string,
  body: Record<string, unknown>,
  onEvent: (event: SSEEvent) => void,
  onDone?: () => void,
  onError?: (err: Error) => void,
): AbortController {
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${API_URL}${path}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `Request failed: ${res.status}`);
      }

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let sseBuffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        sseBuffer += decoder.decode(value, { stream: true });
        const { events, remainder } = parseSSEBuffer(sseBuffer);
        sseBuffer = remainder;

        for (const event of events as SSEEvent[]) {
          onEvent(event);
        }
      }

      onDone?.();
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        onError?.(err as Error);
      }
    }
  })();

  return controller;
}

/**
 * Hook that provides a stable streamSSE function with auto-cleanup on unmount.
 */
export function useCreatorStream() {
  const controllersRef = useRef<AbortController[]>([]);

  const stream = useCallback(
    (
      path: string,
      body: Record<string, unknown>,
      onEvent: (event: SSEEvent) => void,
      onDone?: () => void,
      onError?: (err: Error) => void,
    ) => {
      const ctrl = streamSSE(path, body, onEvent, onDone, onError);
      controllersRef.current.push(ctrl);
      return ctrl;
    },
    [],
  );

  const cancelAll = useCallback(() => {
    controllersRef.current.forEach((c) => c.abort());
    controllersRef.current = [];
  }, []);

  return { stream, cancelAll, uid };
}
