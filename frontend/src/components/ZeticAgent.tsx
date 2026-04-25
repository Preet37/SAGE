"use client";

/**
 * ZeticAgent — offline WebLLM Phi-3.5 fallback (stub).
 *
 * When the network is unreachable or the user opts into private/offline mode,
 * we run Phi-3.5-mini-instruct in the browser via @mlc-ai/web-llm. This file
 * is a stub: the engine is created lazily and only the smallest interface
 * needed by TutorChat is exposed.
 */

import { useCallback, useEffect, useState } from "react";

type Status = "idle" | "loading" | "ready" | "error";

type WebLLMEngine = {
  chat: { completions: { create: (args: unknown) => Promise<unknown> } };
};

const MODEL_ID = "Phi-3.5-mini-instruct-q4f16_1-MLC";

export default function ZeticAgent({
  onReply,
}: {
  onReply?: (text: string) => void;
}) {
  const [status, setStatus] = useState<Status>("idle");
  const [progress, setProgress] = useState(0);
  const [engine, setEngine] = useState<WebLLMEngine | null>(null);

  const load = useCallback(async () => {
    setStatus("loading");
    try {
      const mod = await import("@mlc-ai/web-llm");
      const eng = await mod.CreateMLCEngine(MODEL_ID, {
        initProgressCallback: (r: { progress: number }) => setProgress(r.progress),
      });
      setEngine(eng as unknown as WebLLMEngine);
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  }, []);

  useEffect(() => () => { /* engine has no public dispose; GC handles it */ }, []);

  const askOffline = useCallback(
    async (prompt: string) => {
      if (!engine) return;
      // TODO: stream tokens; for now produce a single completion.
      const res = (await engine.chat.completions.create({
        messages: [
          { role: "system", content: "You are SAGE running offline. Be concise." },
          { role: "user", content: prompt },
        ],
        max_tokens: 256,
      })) as { choices: { message: { content: string } }[] };
      onReply?.(res.choices[0]?.message?.content ?? "");
    },
    [engine, onReply],
  );

  return (
    <div
      className="rounded-2xl p-4"
      style={{ background: "var(--color-muted)", border: "1px solid var(--color-border)" }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold">Offline tutor (ZETIC)</p>
          <p className="text-xs opacity-60">Phi-3.5-mini · runs in your browser</p>
        </div>
        <span
          className="rounded-full px-2 py-0.5 text-xs font-semibold"
          style={{
            background:
              status === "ready" ? "var(--color-secondary)" :
              status === "error" ? "var(--color-destructive)" : "var(--color-border)",
            color: status === "error" ? "white" : "var(--color-foreground)",
          }}
        >
          {status}
        </span>
      </div>

      {status === "idle" && (
        <button onClick={load} className="btn-primary mt-3 w-full">
          Enable offline mode
        </button>
      )}
      {status === "loading" && (
        <div className="mt-3">
          <div className="h-2 w-full overflow-hidden rounded-full" style={{ background: "white" }}>
            <div
              className="h-full"
              style={{ width: `${Math.round(progress * 100)}%`, background: "var(--color-primary)" }}
            />
          </div>
          <p className="mt-1 text-xs opacity-60">
            Downloading model · {Math.round(progress * 100)}%
          </p>
        </div>
      )}
      {status === "ready" && (
        <button
          onClick={() => askOffline("Give me a one-sentence study tip.")}
          className="btn-primary mt-3 w-full"
        >
          Ask offline
        </button>
      )}
    </div>
  );
}
