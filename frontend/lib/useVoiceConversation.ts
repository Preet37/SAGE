"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Conversation } from "@11labs/client";
import type { Mode } from "@11labs/client";
import { useVoiceActions } from "./useVoiceActions";
import { useVoiceStore } from "./useVoiceStore";
import { useRouter } from "next/navigation";
import { API_URL } from "./api";

export type VoiceStatus = "idle" | "connecting" | "connected" | "error";
export type VoiceMode = "listening" | "speaking" | "idle";

export interface VoiceMessage {
  id: string;
  role: "user" | "agent";
  text: string;
  timestamp: number;
}

export interface UseVoiceConversationOptions {
  contextOverride?: string;
}

export function useVoiceConversation(_options: UseVoiceConversationOptions = {}) {
  const [status, setStatus] = useState<VoiceStatus>("idle");
  const [mode, setMode] = useState<VoiceMode>("idle");
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const conversationRef = useRef<Conversation | null>(null);

  const agentId = process.env.NEXT_PUBLIC_ELEVENLABS_AGENT_ID ?? "";
  const router = useRouter();
  const { actions } = useVoiceActions();
  const pageCtx = useVoiceStore();
  // Keep latest refs to avoid stale closures without re-creating the session
  const actionsRef = useRef(actions);
  const pageCtxRef = useRef(pageCtx);
  actionsRef.current = actions;
  pageCtxRef.current = pageCtx;

  const addMessage = useCallback((role: "user" | "agent", text: string) => {
    setMessages((prev) => [
      ...prev,
      { id: `${Date.now()}-${Math.random()}`, role, text, timestamp: Date.now() },
    ]);
  }, []);

  // Detect and execute UI actions from user speech, in background
  const handleUserSpeech = useCallback(async (transcript: string) => {
    const ctx = pageCtxRef.current;
    try {
      const res = await fetch(`${API_URL}/tutor/voice-intent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          transcript,
          page_type: ctx.pageType,
          page_title: ctx.pageTitle,
          topic: ctx.topic,
        }),
      });
      if (!res.ok) return;
      const data = await res.json() as { action: string; path?: string; note_content?: string };
      const { action, path, note_content } = data;

      if (action === "navigate" && path) {
        router.push(path);
      } else if (action === "open_graph") {
        await actionsRef.current.find(a => a.key === "open_graph")?.handler();
      } else if (action === "add_note" && note_content) {
        ctx.sendToTutor?.(note_content);
      } else if (action === "open_quiz") {
        await actionsRef.current.find(a => a.key === "open_quiz")?.handler();
      } else if (action === "open_chat") {
        await actionsRef.current.find(a => a.key === "open_chat")?.handler();
      } else if (action === "mark_complete") {
        await actionsRef.current.find(a => a.key === "mark_complete")?.handler();
      }
    } catch {
      // silent — never interrupt voice session on action detection failure
    }
  }, [router]);

  const startConversation = useCallback(async () => {
    if (conversationRef.current) return;
    setError(null);
    setStatus("connecting");
    setMessages([]);

    // Build clientTools using refs so they always see latest state
    const clientTools: Record<string, (p: Record<string, unknown>) => string | Promise<string>> = {
      navigate_to: async ({ path }: Record<string, unknown>) => {
        if (typeof path === "string") router.push(path);
        return `Navigated to ${path}`;
      },
      get_page_context: () => {
        const ctx = pageCtxRef.current;
        const lines = [
          `Page: ${ctx.pageType || "dashboard"}`,
          ctx.pageTitle && `Title: ${ctx.pageTitle}`,
          ctx.topic && `Topic: ${ctx.topic}`,
          ctx.recentMessages?.length && `Recent chat:\n${ctx.recentMessages.slice(-3).map(m => `${m.role}: ${m.text}`).join("\n")}`,
        ].filter(Boolean);
        return lines.join("\n") || "No page context available";
      },
      send_to_tutor: async ({ message }: Record<string, unknown>) => {
        const ctx = pageCtxRef.current;
        if (typeof message === "string" && ctx.sendToTutor) {
          ctx.sendToTutor(message);
          return `Sent to tutor: "${message}"`;
        }
        return "Could not send to tutor — not on a lesson page";
      },
    };

    // Add all registered page-level actions
    for (const action of actionsRef.current) {
      const handler = action.handler;
      clientTools[action.key] = async (params: Record<string, unknown>) => {
        await handler(params);
        return `Action "${action.key}" executed`;
      };
    }

    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });

      const conversation = await Conversation.startSession({
        agentId,
        connectionType: "webrtc",
        clientTools,
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
          if (source === "user" && message.trim()) {
            handleUserSpeech(message);
          }
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
  }, [agentId, addMessage, router, handleUserSpeech]);

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
