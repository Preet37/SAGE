"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Conversation } from "@11labs/client";
import type { Mode } from "@11labs/client";

export type VoiceStatus = "idle" | "connecting" | "connected" | "error";
export type VoiceMode = "listening" | "speaking" | "idle";

export interface VoiceMessage {
  id: string;
  role: "user" | "agent";
  text: string;
  timestamp: number;
}

export interface UseVoiceConversationOptions {
  /** Context string to inject as the current lesson topic */
  contextOverride?: string;
}

export function useVoiceConversation(options: UseVoiceConversationOptions = {}) {
  const [status, setStatus] = useState<VoiceStatus>("idle");
  const [mode, setMode] = useState<VoiceMode>("idle");
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const conversationRef = useRef<Conversation | null>(null);

  const agentId = process.env.NEXT_PUBLIC_ELEVENLABS_AGENT_ID ?? "";

  const addMessage = useCallback((role: "user" | "agent", text: string) => {
    setMessages((prev) => [
      ...prev,
      { id: `${Date.now()}-${Math.random()}`, role, text, timestamp: Date.now() },
    ]);
  }, []);

  const startConversation = useCallback(async () => {
    if (conversationRef.current) return;
    setError(null);
    setStatus("connecting");
    setMessages([]);

    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });

      const overrides = options.contextOverride
        ? {
            agent: {
              prompt: {
                prompt: `You are SAGE, an AI learning tutor. Current lesson: "${options.contextOverride}". Keep responses to 2-3 sentences. No markdown or bullet points. Respond in the student's language.`,
              },
              firstMessage: `Let's talk about ${options.contextOverride}. What would you like to know?`,
            },
          }
        : undefined;

      const conversation = await Conversation.startSession({
        agentId,
        connectionType: "webrtc",
        ...(overrides ? { overrides } : {}),
        onConnect: () => {
          setStatus("connected");
          setMode("idle");
        },
        onDisconnect: () => {
          setStatus("idle");
          setMode("idle");
          conversationRef.current = null;
        },
        onMessage: ({ message, source }) => {
          addMessage(source === "ai" ? "agent" : "user", message);
        },
        onModeChange: ({ mode: m }: { mode: Mode }) => {
          setMode(m === "speaking" ? "speaking" : m === "listening" ? "listening" : "idle");
        },
        onError: (message: string) => {
          setError(message || "Voice error occurred");
          setStatus("error");
        },
      });

      conversationRef.current = conversation;
    } catch (err) {
      const msg =
        err instanceof DOMException && err.name === "NotAllowedError"
          ? "Microphone access denied. Please allow mic permission and try again."
          : err instanceof Error
          ? err.message
          : "Failed to start voice session";
      setError(msg);
      setStatus("error");
    }
  }, [agentId, addMessage, options.contextOverride]);

  const stopConversation = useCallback(async () => {
    if (conversationRef.current) {
      await conversationRef.current.endSession();
      conversationRef.current = null;
    }
    setStatus("idle");
    setMode("idle");
  }, []);

  const toggleMute = useCallback(async () => {
    if (!conversationRef.current) return;
    const next = !isMuted;
    await conversationRef.current.setMicMuted(next);
    setIsMuted(next);
  }, [isMuted]);

  useEffect(() => {
    return () => {
      conversationRef.current?.endSession().catch(() => null);
    };
  }, []);

  return {
    status,
    mode,
    messages,
    error,
    isMuted,
    isActive: status === "connected",
    startConversation,
    stopConversation,
    toggleMute,
  };
}
