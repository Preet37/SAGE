import { lessonCache } from "./store";
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
        const mod = await import(/* webpackIgnore: true */ "@mlc-ai/web-llm");
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

export interface OfflineChatHandlers {
  onToken: (text: string) => void;
  onDone: () => void;
  onError: (err: unknown) => void;
}

export function runOfflineChat(
  lessonId: number,
  message: string,
  history: { role: "user" | "assistant"; content: string }[],
  keyConcepts: string[],
  handlers: OfflineChatHandlers,
): () => void {
  let aborted = false;

  (async () => {
    try {
      const cached = await lessonCache.get(lessonId);
      const chunks = cached ? retrieveTopK(message, cached.chunks) : [];
      const context = chunks.length
        ? chunks.map((c, i) => `[${i + 1}] ${c}`).join("\n\n")
        : keyConcepts.length
          ? `Key concepts: ${keyConcepts.join(", ")}`
          : "No lesson context available offline.";

      const system = `You are SAGE, a Socratic AI tutor running fully offline in the learner's browser. Guide learners through discovery using probing questions — never give direct answers. Always end your response with a question. Be concise and encouraging.

Lesson context:
${context}`;

      const msgs: ChatMessage[] = [{ role: "system", content: system }];
      for (const turn of history.slice(-8)) {
        msgs.push({ role: turn.role, content: turn.content });
      }
      msgs.push({ role: "user", content: message });

      const engine = await loadEngine();
      if (aborted) return;

      const stream = await engine.chat.completions.create({
        messages: msgs,
        stream: true,
        max_tokens: 512,
        temperature: 0.7,
      });

      for await (const chunk of stream) {
        if (aborted) break;
        const delta = chunk.choices[0]?.delta?.content ?? "";
        if (delta) handlers.onToken(delta);
      }

      if (!aborted) handlers.onDone();
    } catch (err) {
      if (!aborted) handlers.onError(err);
    }
  })();

  return () => { aborted = true; };
}
