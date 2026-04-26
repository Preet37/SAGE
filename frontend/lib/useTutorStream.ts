"use client";
import { useState, useCallback, useRef } from "react";
import { getToken } from "./auth";
import { API_URL } from "./api";

/** uid() requires a secure context (HTTPS/localhost).
 *  Fall back to getRandomValues for plain-HTTP deployments. */
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

export interface Verification {
  score: number;
  label: "grounded" | "partial" | "unverified";
  grounded_claims: string[];
  unsupported_claims: string[];
  rationale: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  verification?: Verification;
}

export interface ToolCallState {
  name: string;
  result?: unknown;
}

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
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

export function useTutorStream(lessonId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [toolResults, setToolResults] = useState<ToolResultMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [toolCall, setToolCall] = useState<ToolCallState | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesRef = useRef<Message[]>(messages);
  const sessionIdRef = useRef<string | null>(null);

  // Keep ref in sync with state so sendMessage always reads the latest
  const updateMessages = useCallback((updater: Message[] | ((prev: Message[]) => Message[])) => {
    setMessages((prev) => {
      const next = typeof updater === "function" ? updater(prev) : updater;
      messagesRef.current = next;
      return next;
    });
  }, []);

  const sendMessage = useCallback(
    async (content: string, mode = "default") => {
      const userMsg: Message = {
        id: uid(),
        role: "user",
        content,
      };

      const allMessages = [...messagesRef.current, userMsg];
      updateMessages(allMessages);
      setStreaming(true);
      setToolCall(null);

      const assistantId = uid();
      let assistantText = "";

      // Add placeholder immediately so error messages have a bubble to land in
      updateMessages((prev) => [
        ...prev,
        { id: assistantId, role: "assistant", content: "" },
      ]);

      try {
        // Backend expects: lesson_id (int), message (str), history (prev msgs), teaching_mode
        const messages = allMessages.map((m) => ({ role: m.role, content: m.content }));
        const res = await fetch(`${API_URL}/tutor/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify({
            lesson_id: lessonId,
            messages,
            mode,
            session_id: sessionIdRef.current ?? null,
          }),
        });

        if (res.status === 401) {
          if (typeof window !== "undefined") {
            localStorage.removeItem("tutor_token");
            const returnTo = window.location.pathname;
            window.location.href = `/login?returnTo=${encodeURIComponent(returnTo)}`;
          }
          return;
        }

        if (!res.ok) throw new Error(`Stream request failed (${res.status})`);

        const returnedSessionId = res.headers.get("X-Session-Id");
        if (returnedSessionId) {
          sessionIdRef.current = returnedSessionId;
          setSessionId(returnedSessionId);
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
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: assistantText } : m
                )
              );
            } else if (evtType === "done") {
              const v = evtData.verification as Record<string, unknown> | undefined;
              if (v) {
                const verification: Verification = {
                  score: (v.score as number) ?? 1.0,
                  label: (v.passed as boolean) ? "grounded" : "unverified",
                  grounded_claims: [],
                  unsupported_claims: [],
                  rationale: "",
                };
                updateMessages((prev) =>
                  prev.map((m) => m.id === assistantId ? { ...m, verification } : m)
                );
              }
            } else if (evtType === "error") {
              const errorMsg = (evtData.message as string) || "Something went wrong. Please try again.";
              assistantText = assistantText
                ? `${assistantText}\n\n---\n\n*${errorMsg}*`
                : errorMsg;
              updateMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: assistantText } : m
                )
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
    [lessonId, updateMessages]
  );

  const loadHistory = useCallback((history: Message[], sid: string | null = null) => {
    updateMessages(history);
    setToolResults([]);
    sessionIdRef.current = sid;
    setSessionId(sid);
  }, [updateMessages]);

  const clearMessages = useCallback(() => {
    updateMessages([]);
    setToolResults([]);
    sessionIdRef.current = null;
    setSessionId(null);
  }, [updateMessages]);

  return { messages, toolResults, streaming, toolCall, sessionId, sendMessage, loadHistory, clearMessages, setSessionId };
}
