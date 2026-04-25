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
          // ignore malformed lines
        }
      }
    }
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

      const apiMessages = allMessages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const assistantId = uid();
      let assistantText = "";

      try {
        const body: Record<string, unknown> = { messages: apiMessages, mode };
        if (sessionId) body.session_id = sessionId;

        const res = await fetch(`${API_URL}/explore/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify(body),
        });

        if (!res.ok) throw new Error("Stream request failed");

        // Capture session ID from response header for subsequent requests
        const newSessionId = res.headers.get("X-Session-Id");
        if (newSessionId) setSessionId(newSessionId);

        const reader = res.body!.getReader();
        const decoder = new TextDecoder();
        let sseBuffer = "";

        updateMessages((prev) => [
          ...prev,
          { id: assistantId, role: "assistant", content: "" },
        ]);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          sseBuffer += decoder.decode(value, { stream: true });
          const { events, remainder } = parseSSEBuffer(sseBuffer);
          sseBuffer = remainder;

          for (const event of events as Record<string, unknown>[]) {
            if (event.type === "text") {
              assistantText += event.delta as string;
              updateMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: assistantText } : m
                )
              );
            } else if (event.type === "tool_call") {
              setToolCall({ name: event.name as string });
            } else if (event.type === "tool_result") {
              setToolCall(null);
              setToolResults((prev) => [
                ...prev,
                {
                  id: uid(),
                  type: "tool_result",
                  toolName: event.name as string,
                  result: event.result,
                },
              ]);
            } else if (event.type === "error") {
              const errorMsg = (event.message as string) || "Something went wrong. Please try again.";
              if (assistantText) {
                assistantText += `\n\n---\n\n*${errorMsg}*`;
              } else {
                assistantText = errorMsg;
              }
              updateMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId ? { ...m, content: assistantText } : m
                )
              );
            } else if (event.type === "done") {
              // streaming complete
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
    [sessionId, updateMessages]
  );

  const loadSession = useCallback((id: string, history: Message[]) => {
    setSessionId(id);
    updateMessages(history);
    setToolResults([]);
  }, [updateMessages]);

  const startNewSession = useCallback(() => {
    setSessionId(null);
    updateMessages([]);
    setToolResults([]);
  }, [updateMessages]);

  return {
    messages,
    toolResults,
    streaming,
    toolCall,
    sessionId,
    sendMessage,
    loadSession,
    startNewSession,
  };
}
