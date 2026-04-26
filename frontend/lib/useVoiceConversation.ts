"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Conversation } from "@11labs/client";
import type { Mode } from "@11labs/client";
import { useVoiceActions } from "./useVoiceActions";
import { useVoiceStore } from "./useVoiceStore";
import { useRouter } from "next/navigation";

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
  const { actions, invoke } = useVoiceActions();
  const pageCtx = useVoiceStore();

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

    // Build clientTools from registered page actions
    const clientTools: Record<string, (p: Record<string, unknown>) => string | Promise<string>> = {
      navigate_to: async ({ path }: Record<string, unknown>) => {
        if (typeof path === "string") router.push(path);
        return `Navigated to ${path}`;
      },
      get_page_context: () => {
        const lines = [
          `Page: ${pageCtx.pageType}`,
          pageCtx.pageTitle && `Title: ${pageCtx.pageTitle}`,
          pageCtx.topic && `Topic: ${pageCtx.topic}`,
          pageCtx.recentMessages?.length && `Recent chat:\n${pageCtx.recentMessages.slice(-3).map(m => `${m.role}: ${m.text}`).join("\n")}`,
        ].filter(Boolean);
        return lines.join("\n") || "No page context available";
      },
      send_to_tutor: async ({ message }: Record<string, unknown>) => {
        if (typeof message === "string" && pageCtx.sendToTutor) {
          pageCtx.sendToTutor(message);
          return `Sent to tutor: "${message}"`;
        }
        return "Could not send to tutor — not on a lesson page";
      },
    };

    // Add all registered page-level actions
    for (const action of actions) {
      clientTools[action.key] = async (params: Record<string, unknown>) => {
        await action.handler(params);
        return `Action "${action.key}" executed`;
      };
    }

    // Build dynamic system prompt with available actions
    const actionList = [
      "navigate_to(path) — go to a page (e.g. /explore, /learn, /network, /pocket, /sketch)",
      "get_page_context() — see what's currently on the user's screen",
      "send_to_tutor(message) — inject a message into the tutor chat",
      ...actions.map((a) => `${a.key}() — ${a.description}`),
    ].join("\n- ");

    const systemPromptAddition = `
You are SAGE, an interactive AI tutor. You are a VOICE INTERFACE that is also EMBEDDED IN THE APP.
You can see and control the student's screen using these tools:
- ${actionList}

Current screen context: ${pageCtx.pageType || "unknown page"} — "${pageCtx.pageTitle || ""}"
${pageCtx.topic ? `Topic: ${pageCtx.topic}` : ""}

When the user asks you to "show the graph", "open the simulation", or similar — call the appropriate action tool.
When explaining a concept, also call send_to_tutor() to leave written notes for the user.
Always be interactive — don't just talk, DO things.`.trim();

    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });

      const conversation = await Conversation.startSession({
        agentId,
        connectionType: "webrtc",
        clientTools,
        overrides: {
          agent: {
            prompt: { prompt: systemPromptAddition },
          },
        },
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
  }, [agentId, addMessage, actions, invoke, router, pageCtx]);

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
