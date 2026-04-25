import type { AgentEvent, DoneEvent, SSEHandlers, TokenEvent } from "@/lib/api";

import { lessonStore } from "./store";
import { retrieveTopK } from "./retriever";

const MODEL_ID = "Phi-3.5-mini-instruct-q4f16_1-MLC";

type ChatMessage = { role: string; content: string };

type MLCEngine = {
  chat: {
    completions: {
      create: (args: {
        messages: ChatMessage[];
        stream: true;
        max_tokens?: number;
        temperature?: number;
      }) => Promise<AsyncIterable<{ choices: { delta: { content?: string } }[] }>>;
    };
  };
};

export type ModelStatus = "idle" | "loading" | "ready" | "error";

type ProgressCallback = (progress: number, status: ModelStatus) => void;

let engineSingleton: Promise<MLCEngine> | null = null;

export async function loadEngine(onProgress?: ProgressCallback): Promise<MLCEngine> {
  if (!engineSingleton) {
    engineSingleton = (async () => {
      onProgress?.(0, "loading");
      try {
        const mod = await import("@mlc-ai/web-llm");
        const eng = await mod.CreateMLCEngine(MODEL_ID, {
          initProgressCallback: (r: { progress: number }) =>
            onProgress?.(r.progress, "loading"),
        });
        onProgress?.(1, "ready");
        return eng as unknown as MLCEngine;
      } catch (err) {
        engineSingleton = null;
        onProgress?.(0, "error");
        throw err;
      }
    })();
  }
  return engineSingleton;
}

export function isEngineLoaded(): boolean {
  return engineSingleton !== null;
}

function buildMessages(
  chunks: string[],
  history: { role: "user" | "sage"; text: string }[],
  message: string,
): ChatMessage[] {
  const context = chunks.length
    ? chunks.map((c, i) => `[${i + 1}] ${c}`).join("\n\n")
    : "No lesson content available offline.";

  const system = `You are SAGE, a Socratic AI tutor running fully offline in the learner's browser. Your role is to guide learners through discovery using probing questions — never give direct answers. Always end your response with a question. Be concise and encouraging.

Lesson context:
${context}`;

  const msgs: ChatMessage[] = [{ role: "system", content: system }];

  for (const turn of history.slice(-8)) {
    msgs.push({ role: turn.role === "user" ? "user" : "assistant", content: turn.text });
  }

  msgs.push({ role: "user", content: message });
  return msgs;
}

export function runOfflineChat(
  lessonId: number,
  sessionId: number,
  message: string,
  history: { role: "user" | "sage"; text: string }[],
  handlers: SSEHandlers,
): () => void {
  let aborted = false;

  handlers.onAgent?.({ agent: "socratic", phase: "start" } satisfies AgentEvent);

  (async () => {
    try {
      const cached = await lessonStore.get(lessonId);
      const chunks = cached ? retrieveTopK(message, cached.chunks) : [];

      handlers.onAgent?.({ agent: "retriever", phase: "done", k: chunks.length } satisfies AgentEvent);
      handlers.onAgent?.({ agent: "socratic", phase: "generating" } satisfies AgentEvent);

      const engine = await loadEngine();
      if (aborted) return;

      const stream = await engine.chat.completions.create({
        messages: buildMessages(chunks, history, message),
        stream: true,
        max_tokens: 512,
        temperature: 0.7,
      });

      for await (const chunk of stream) {
        if (aborted) break;
        const delta = chunk.choices[0]?.delta?.content ?? "";
        if (delta) {
          handlers.onToken?.({ agent: "socratic", text: delta } satisfies TokenEvent);
        }
      }

      if (!aborted) {
        handlers.onDone?.({ session_id: sessionId, ok: true, grounded: false } satisfies DoneEvent);
      }
    } catch (err) {
      if (!aborted) handlers.onError?.(err);
    }
  })();

  return () => {
    aborted = true;
  };
}
