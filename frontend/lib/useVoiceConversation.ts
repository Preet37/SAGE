"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Conversation } from "@11labs/client";
import type { Mode } from "@11labs/client";
import { useVoiceStore } from "./useVoiceStore";

export type VoiceStatus = "idle" | "connecting" | "connected" | "error";
export type VoiceMode = "listening" | "speaking" | "idle";

export interface VoiceMessage {
  id: string;
  role: "user" | "agent";
  text: string;
  timestamp: number;
}

export interface UseVoiceConversationOptions {
  /** Optional manual context override (e.g. from a specific lesson component) */
  contextOverride?: string;
}

export function useVoiceConversation(options: UseVoiceConversationOptions = {}) {
  const [status, setStatus] = useState<VoiceStatus>("idle");
  const [mode, setMode] = useState<VoiceMode>("idle");
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const conversationRef = useRef<Conversation | null>(null);
  const router = useRouter();
  const { context } = useVoiceStore();

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

      // Build a rich context-aware system prompt from the current page state
      const manualContext = options.contextOverride;
      const pageSummary = manualContext
        ? `The student is currently studying: "${manualContext}".`
        : `The student is on the ${context.pageType} page — "${context.title}". ${context.description}${context.currentTopic ? ` Current topic: ${context.currentTopic}.` : ""}${context.recentMessages ? ` Recent conversation:\n${context.recentMessages}` : ""}`;

      const systemPrompt = `You are SAGE, an intelligent AI learning assistant embedded directly in the SAGE learning platform.

CURRENT CONTEXT:
${pageSummary}

You can actively help the student by:
- Answering questions about what they are looking at
- Sending messages to the tutor chat on their behalf using the send_to_tutor tool
- Navigating to other pages using the navigate_to tool
- Explaining content that is currently visible

IMPORTANT:
- Keep responses concise (2-4 sentences) — this is a voice interaction
- No markdown, bullet points, or asterisks — speak in natural sentences
- Always refer to the current page context when relevant
- Respond in the same language as the student`;

      const firstMessage = manualContext
        ? `Let me help you with ${manualContext}. What would you like to know?`
        : context.pageType === "lesson"
        ? `I can see you're studying "${context.title}". Want me to explain something, answer a question, or help you through this lesson?`
        : `I'm SAGE, your voice learning assistant. You're on the ${context.title} page. What can I help you with?`;

      const conversation = await Conversation.startSession({
        agentId,
        connectionType: "websocket",
        overrides: {
          agent: {
            prompt: { prompt: systemPrompt },
            firstMessage,
          },
        },
        // Client tools the voice agent can call to interact with the UI
        clientTools: {
          navigate_to: ({ path }: { path: string }) => {
            try {
              router.push(path);
              return `Navigating to ${path}`;
            } catch {
              return "Navigation failed";
            }
          },
          send_to_tutor: ({ message }: { message: string }) => {
            if (context.sendToTutor) {
              context.sendToTutor(message);
              return `Sent to tutor: "${message}"`;
            }
            return "No active tutor session on this page";
          },
          get_page_context: () => {
            return JSON.stringify({
              page: context.pageType,
              title: context.title,
              topic: context.currentTopic || context.title,
              description: context.description,
              recentMessages: context.recentMessages?.slice(-500) || "",
            });
          },
          search_concept: ({ topic }: { topic: string }) => {
            router.push(`/explore?q=${encodeURIComponent(topic)}`);
            return `Opening deep dive for "${topic}"`;
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
  }, [agentId, addMessage, context, options.contextOverride, router]);

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
