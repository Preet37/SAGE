"use client";
import { useState, useCallback, useRef } from "react";
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

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export interface ToolCallState {
  name: string;
  result?: unknown;
}

export interface ToolResultMessage {
  id: string;
  type: "tool_result";
  toolName: string;
  result: unknown;
}

interface SSEEvent {
  name: string;
  data: Record<string, unknown>;
}

function parseSSEBuffer(buffer: string): { events: SSEEvent[]; remainder: string } {
  const events: SSEEvent[] = [];
  const parts = buffer.split("\n\n");
  const remainder = parts.pop() ?? "";
  for (const part of parts) {
    let name = "message";
    let data: Record<string, unknown> | null = null;
    for (const line of part.split("\n")) {
      if (line.startsWith("event: ")) {
        name = line.slice(7).trim();
      } else if (line.startsWith("data: ")) {
        try {
          data = JSON.parse(line.slice(6)) as Record<string, unknown>;
        } catch {
          // ignore malformed lines
        }
      }
    }
    if (data !== null) events.push({ name, data });
  }
  return { events, remainder };
}


export function useExploreStream() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [toolResults, setToolResults] = useState<ToolResultMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [toolCall, setToolCall] = useState<ToolCallState | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesRef = useRef<Message[]>(messages);
  const sessionIdRef = useRef<string | null>(null);

  const updateMessages = useCallback((updater: Message[] | ((prev: Message[]) => Message[])) => {
    setMessages((prev) => {
      const next = typeof updater === "function" ? updater(prev) : updater;
      messagesRef.current = next;
      return next;
    });
  }, []);

  const sendMessage = useCallback(
    async (content: string, mode = "default") => {
      const userMsg: Message = { id: uid(), role: "user", content };
      const allMessages = [...messagesRef.current, userMsg];
      updateMessages(allMessages);
      setStreaming(true);
      setToolCall(null);

      const assistantId = uid();
      let assistantText = "";

      updateMessages((prev) => [
        ...prev,
        { id: assistantId, role: "assistant", content: "" },
      ]);

      try {
        const messages = allMessages.map((m) => ({ role: m.role, content: m.content }));

        const res = await fetch(`${API_URL}/explore/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify({
            messages,
            mode,
            session_id: sessionIdRef.current ?? null,
          }),
        });

        if (res.status === 401) {
          if (typeof window !== "undefined") {
            localStorage.removeItem("tutor_token");
            window.location.href = `/login?returnTo=${encodeURIComponent(window.location.pathname)}`;
          }
          return;
        }

        if (!res.ok) throw new Error(`Stream request failed (${res.status})`);

        const newSessionId = res.headers.get("X-Session-Id");
        if (newSessionId) {
          sessionIdRef.current = newSessionId;
          setSessionId(newSessionId);
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

          for (const { data: evtData } of events) {
            const evtType = evtData.type as string | undefined;
            if (evtType === "text") {
              assistantText += (evtData.delta as string) || "";
              updateMessages((prev) =>
                prev.map((m) => m.id === assistantId ? { ...m, content: assistantText } : m)
              );
            } else if (evtType === "error") {
              const errorMsg = (evtData.message as string) || "Something went wrong. Please try again.";
              assistantText = assistantText
                ? `${assistantText}\n\n---\n\n*${errorMsg}*`
                : errorMsg;
              updateMessages((prev) =>
                prev.map((m) => m.id === assistantId ? { ...m, content: assistantText } : m)
              );
            } else if (evtType === "tool_call") {
              setToolCall({ name: evtData.name as string });
            } else if (evtType === "tool_result") {
              setToolCall(null);
              setToolResults((prev) => [
                ...prev,
                { id: uid(), type: "tool_result", toolName: evtData.name as string, result: evtData.result },
              ]);
            }
          }
        }
      } catch (err) {
        console.error("Stream error:", err);
        updateMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, content: "Sorry, something went wrong. Please try again." }
              : m
          )
        );
      } finally {
        setStreaming(false);
        setToolCall(null);
      }
    },
    [updateMessages]
  );

  const loadSession = useCallback((id: string, history: Message[]) => {
    sessionIdRef.current = id;
    setSessionId(id);
    updateMessages(history);
    setToolResults([]);
  }, [updateMessages]);

  const startNewSession = useCallback(() => {
    sessionIdRef.current = null;
    setSessionId(null);
    updateMessages([]);
    setToolResults([]);
  }, [updateMessages]);

  return { messages, toolResults, streaming, toolCall, sessionId, sendMessage, loadSession, startNewSession };
}
